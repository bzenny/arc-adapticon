"""P004 acceptance tests T01-T15 for the ARC Scout local inventory engine."""

from __future__ import annotations

import ast
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from arc_scout import inventory as inv
from tests import fixtures as fx

REPO_ROOT = Path(__file__).resolve().parent.parent
PKG = REPO_ROOT / "arc_scout"


def cli(*args: str, env: dict | None = None, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess:
    base = {"PATH": os.environ.get("PATH", os.defpath), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(REPO_ROOT)}
    return subprocess.run([sys.executable, "-m", "arc_scout", *args], capture_output=True, cwd=cwd,
                          env={**base, **(env or {})})


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.f = fx.standard_fixture(self.root)
        self.git_dir = self.f["git_dir"]
        self.out = self.root / "out"
        self.out.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def scan(self, commit=None, **kw):
        return inv.inventory(self.git_dir, self.f["c2"] if commit is None else commit, **kw)

    def assertFails(self, code, commit=None, **kw):
        with self.assertRaises(inv.ScoutError) as cm:
            self.scan(commit, **kw)
        self.assertEqual(cm.exception.code, code, cm.exception.message)
        return cm.exception


class T01ExactInventory(Base):
    def test_manifest_matches_independent_expectation(self):
        m = self.scan()
        entries = fx.expected_entries(self.f["v2"])
        omissions = [{"path": e["path"], "reason": e["omission_reason"]} for e in entries if e["disposition"] == "omitted"]
        included = [e for e in entries if e["disposition"] == "included"]
        expected = {
            "schema_version": "0.1.0",
            "tool": {"name": "arc-scout", "version": "0.1.0"},
            "status": "complete",
            "subject": {"commit": self.f["c2"], "object_format": "sha1"},
            "policy": {"max_path_bytes": 4096, "max_component_bytes": 255},
            "coverage": {"tree_entries": len(entries), "included": len(included), "omitted": len(omissions),
                         "included_bytes": sum(e["size_bytes"] for e in included)},
            "entries": entries,
            "omissions": omissions,
            "assessment": {"license": "unknown", "dependencies": "unknown", "runtime": "not_verified"},
            "limitations": list(inv.LIMITATIONS),
        }
        self.assertEqual(m, expected)
        self.assertEqual(m["coverage"], {"tree_entries": 10, "included": 7, "omitted": 3,
                                         "included_bytes": expected["coverage"]["included_bytes"]})

    def test_cli_writes_same_manifest(self):
        out = self.out / "m.json"
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(out.read_bytes(), inv.serialize(self.scan()))


class T02Deterministic(Base):
    def test_repeated_runs_byte_identical(self):
        a, b, c = (self.out / n for n in ("a.json", "b.json", "c.json"))
        for path, cwd in ((a, REPO_ROOT), (b, REPO_ROOT), (c, self.root)):
            r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(path),
                    env={"GIT_DIR": "/nonexistent", "LANG": "de_DE.UTF-8", "TZ": "Asia/Tokyo"}, cwd=cwd)
            self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(a.read_bytes(), b.read_bytes())
        self.assertEqual(a.read_bytes(), c.read_bytes())

    def test_no_timestamps_or_absolute_paths_in_canonical_manifest(self):
        out, rec = self.out / "m.json", self.out / "run.json"
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out),
                "--run-record", str(rec))
        self.assertEqual(r.returncode, 0, r.stderr)
        text = out.read_text()
        self.assertNotIn(str(self.root), text)
        self.assertNotRegex(text, r"\d{4}-\d{2}-\d{2}T\d{2}:")
        self.assertIn("started_at", json.loads(rec.read_text()))

    def test_ordering_is_bytewise_by_path(self):
        paths = [e["path"].encode() for e in self.scan()["entries"]]
        self.assertEqual(paths, sorted(paths))


class T03HistoricalCommit(Base):
    def test_pinned_older_commit(self):
        m = self.scan(self.f["c1"])
        self.assertEqual(m["subject"]["commit"], self.f["c1"])
        self.assertEqual(m["entries"], fx.expected_entries(self.f["v1"]))
        self.assertNotIn("run.sh", [e["path"] for e in m["entries"]])

    def test_commit_id_computed_independently(self):
        # v1 has no machine-specific bytes: recompute its commit ID from raw object formats.
        import hashlib

        def obj(kind, body):
            return hashlib.sha1(b"%s %d\0" % (kind, len(body)) + body)

        src = obj(b"tree", b"100644 app.py\0" + bytes.fromhex(fx.blob_id(self.f["v1"]["src"]["app.py"]))).hexdigest()
        root = obj(b"tree", b"100644 README.md\0" + bytes.fromhex(fx.blob_id(self.f["v1"]["README.md"]))
                   + b"40000 src\0" + bytes.fromhex(src)).hexdigest()
        who = b"Fixture <fixture@example.invalid> 1700000000 +0000"
        commit = obj(b"commit", b"tree %s\nauthor %s\ncommitter %s\n\nv1\n" % (root.encode(), who, who)).hexdigest()
        self.assertEqual(self.f["c1"], commit)
        self.assertEqual(self.scan(commit)["subject"]["commit"], commit)


class T04InvalidCommits(Base):
    def test_rejects_non_full_sha_forms(self):
        c2 = self.f["c2"]
        for bad in ("main", "HEAD", "refs/heads/main", c2[:7], c2[:39], c2 + "0", c2.upper(),
                    f"{c2}^{{tree}}", f"{c2}~1", "", " " + c2, c2 + "\n", "-p"):
            with self.subTest(bad=bad):
                self.assertFails("invalid_commit_id", bad)

    def test_nonexistent_commit(self):
        self.assertFails("commit_not_found", "0" * 40)

    def test_non_commit_objects(self):
        repo = self.f["repo"]
        blob = repo.blob(b"just a blob\n")
        tree = repo.tree({"a": b"a\n"})
        tag = fx.git(self.git_dir, "hash-object", "-t", "tag", "-w", "--stdin", data=(
            f"object {self.f['c2']}\ntype commit\ntag v1\ntagger Fixture <f@example.invalid> 1700000000 +0000\n\nv1\n"
        ).encode()).decode().strip()
        for oid, kind in ((blob, "blob"), (tree, "tree"), (tag, "tag")):
            with self.subTest(kind=kind):
                e = self.assertFails("not_a_commit", oid)
                self.assertIn(kind, e.message)

    def test_missing_object(self):
        repo = self.f["repo"]
        c = repo.commit(repo.tree({"gone.txt": ("missing_blob", "ab" * 20)}), "missing\n")
        self.assertFails("missing_object", c)

    def test_not_a_git_dir(self):
        empty = self.root / "empty"
        empty.mkdir()
        with self.assertRaises(inv.ScoutError) as cm:
            inv.inventory(empty, self.f["c2"])
        self.assertEqual(cm.exception.code, "not_a_git_dir")
        with self.assertRaises(inv.ScoutError) as cm:
            inv.inventory(self.root / "absent", self.f["c2"])
        self.assertEqual(cm.exception.code, "not_a_git_dir")


class T05MissingGit(Base):
    def test_explicit_missing_executable(self):
        self.assertFails("git_not_found", git_executable=str(self.root / "no-such-git"))

    def test_git_not_on_path(self):
        with mock.patch("shutil.which", return_value=None):
            self.assertFails("git_not_found")

    def test_cli_reports_git_not_found(self):
        out = self.out / "m.json"
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out),
                "--git", str(self.root / "no-such-git"))
        self.assertEqual(r.returncode, 1)
        self.assertIn(b"git_not_found", r.stderr)
        self.assertEqual(json.loads(out.read_text())["error"]["code"], "git_not_found")


class T06UnsafePaths(Base):
    def test_unsafe_names_are_omitted_with_reasons(self):
        repo = self.f["repo"]
        spec = {
            "ok.txt": b"ok\n",
            "..": {"escape.txt": b"x\n"},
            ".git": {"config": b"[core]\n"},
            ".GIT": {"hooks": b"x\n"},
            "a\\b.txt": b"x\n",
            b"ctl\x01.txt": b"x\n",
            b"bad\xff.txt": b"x\n",
            ".": {"dot.txt": b"x\n"},
            "deep": {"dir": {"file.txt": b"x\n"}},
        }
        c = repo.commit(repo.tree(spec), "unsafe\n")
        m = self.scan(c, limits=inv.Limits(max_path_bytes=14))
        by = {(e["path"] if e["path"] is not None else e["path_hex"]): e for e in m["entries"]}
        self.assertEqual(m["status"], "complete")
        self.assertEqual(by["ok.txt"]["disposition"], "included")
        for p in ("../escape.txt", ".git/config", ".GIT/hooks", "a\\b.txt", "ctl\x01.txt", "./dot.txt"):
            with self.subTest(path=p):
                self.assertEqual(by[p]["omission_reason"], "unsafe_path")
        self.assertEqual(by[b"bad\xff.txt".hex()]["omission_reason"], "path_not_utf8")
        self.assertIsNone(by[b"bad\xff.txt".hex()]["path"])
        self.assertEqual(by["deep/dir/file.txt"]["omission_reason"], "path_too_long")
        self.assertEqual(m["coverage"]["included"], 1)
        self.assertEqual(len(m["omissions"]), len(spec) - 1)

    def test_classify_path_rules(self):
        lim = inv.Limits()
        for raw, reason in ((b"a/b", None), (b"/abs", "unsafe_path"), (b"a//b", "unsafe_path"),
                            (b"a/../b", "unsafe_path"), (b"x/.Git/y", "unsafe_path"), (b"del\x7f", "unsafe_path"),
                            (b"a" * 256, "path_too_long"), (b"\xc3\x28", "path_not_utf8")):
            with self.subTest(raw=raw):
                self.assertEqual(inv.classify_path(raw, lim)[1], reason)


class T07LinksNotFollowed(Base):
    def test_symlinks_and_gitlinks_omitted_and_not_followed(self):
        m = self.scan()
        by = {e["path"]: e for e in m["entries"]}
        self.assertEqual(by["link"]["omission_reason"], "symlink_not_followed")
        self.assertEqual(by["etc_link"]["omission_reason"], "symlink_not_followed")
        self.assertEqual(by["vendor/lib"]["omission_reason"], "gitlink_not_followed")
        self.assertIsNone(by["vendor/lib"]["size_bytes"])
        # Nothing resolved through the link: no README or /etc/passwd metadata attached to it.
        self.assertEqual(by["link"]["size_bytes"], len(b"README.md"))
        self.assertEqual(by["etc_link"]["size_bytes"], len(b"/etc/passwd"))
        # The gitlink target does not exist in the repository; Scout never asked for it.
        self.assertNotIn("1234567890abcdef1234567890abcdef12345678/", json.dumps(m))


class T08Limits(Base):
    def test_entry_limit(self):
        self.assertFails("entry_limit", limits=inv.Limits(max_entries=3))

    def test_output_limit(self):
        self.assertFails("output_limit", limits=inv.Limits(max_git_output_bytes=100))

    def test_timeout_kills_git(self):
        slow = self.root / "slow-git"
        slow.write_text("#!/bin/sh\nsleep 30 &\nwait\n")
        slow.chmod(0o755)
        import time
        t0 = time.monotonic()
        self.assertFails("timeout", git_executable=str(slow), limits=inv.Limits(timeout_seconds=0.5))
        self.assertLess(time.monotonic() - t0, 10)

    def test_path_and_component_limits(self):
        repo = self.f["repo"]
        c = repo.commit(repo.tree({"x" * 300: b"x\n", "y": b"y\n"}), "long\n")
        m = self.scan(c)
        self.assertEqual({e["path"][:1]: e["disposition"] for e in m["entries"]}, {"x": "omitted", "y": "included"})


class T09HostileReadme(Base):
    def test_readme_instructions_not_processed(self):
        out = self.out / "m.json"
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        text = out.read_text()
        self.assertNotIn("ignore previous", text.lower())
        m = json.loads(text)
        self.assertEqual(m["assessment"]["license"], "unknown")
        self.assertTrue(out.exists())
        self.assertEqual(list(self.f["markers"].iterdir()), [])


class T10Canaries(Base):
    def test_repository_and_git_dir_canaries_never_run(self):
        names = fx.install_git_dir_canaries(self.git_dir, self.f["markers"])
        self.assertGreater(len(names), 0)
        for commit in (self.f["c2"], self.f["c1"], "0" * 40, "main"):
            try:
                self.scan(commit)
            except inv.ScoutError:
                pass
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output",
                str(self.out / "m.json"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(sorted(p.name for p in self.f["markers"].iterdir()), [])

    def test_canaries_are_live(self):
        # Control: the canary scripts do leave markers when actually executed.
        script = self.root / "probe.sh"
        script.write_bytes(fx.canary_script(self.f["markers"], "probe"))
        subprocess.run(["/bin/sh", str(script)], check=True)
        self.assertTrue((self.f["markers"] / "probe").exists())


class T11SubjectUnchanged(Base):
    def test_git_dir_byte_identical_after_scans(self):
        fx.install_git_dir_canaries(self.git_dir, self.f["markers"])
        before = fx.snapshot(self.git_dir)
        self.scan()
        self.scan(self.f["c1"])
        for bad in ("0" * 40, "nope"):
            r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", bad, "--output", str(self.out / "f.json"))
            self.assertEqual(r.returncode, 1)
        self.assertEqual(fx.snapshot(self.git_dir), before)

    def test_output_inside_subject_rejected(self):
        before = fx.snapshot(self.git_dir)
        for target in (self.git_dir / "m.json", self.git_dir / "objects" / "m.json"):
            r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(target))
            self.assertEqual(r.returncode, 2)
            self.assertFalse(target.exists())
        self.assertEqual(fx.snapshot(self.git_dir), before)

    def test_worktree_of_dot_git_counts_as_subject(self):
        work = self.root / "work"
        (work / ".git").mkdir(parents=True)
        self.assertTrue(inv.output_inside_subject(work / "m.json", (work / ".git").resolve()))
        self.assertFalse(inv.output_inside_subject(self.out / "m.json", (work / ".git").resolve()))


class T12Offline(Base):
    def test_no_network_modules_imported(self):
        banned = {"socket", "ssl", "http", "urllib", "ftplib", "smtplib", "requests", "asyncio"}
        for path in PKG.glob("*.py"):
            tree = ast.parse(path.read_text())
            names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names |= {a.name.split(".")[0] for a in node.names}
                elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                    names.add(node.module.split(".")[0])
            with self.subTest(file=path.name):
                self.assertFalse(names & banned, names & banned)

    def test_environment_is_not_inherited(self):
        hostile = {"HTTPS_PROXY": "http://proxy.invalid", "GIT_DIR": "/x", "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/y",
                   "GIT_CONFIG_PARAMETERS": "'core.fsmonitor=/z'", "GIT_ASKPASS": "/w", "SSH_ASKPASS": "/v"}
        with mock.patch.dict(os.environ, hostile):
            env = inv.sanitized_environment()
            self.scan()
        self.assertFalse(set(hostile) & set(env))
        self.assertEqual(env["GIT_TERMINAL_PROMPT"], "0")
        self.assertIn("protocol.allow=never", inv.GIT_GLOBAL_OPTIONS)

    def test_partial_clone_rejected(self):
        with open(self.git_dir / "config", "a") as fh:
            fh.write('[remote "origin"]\n\turl = https://example.invalid/r.git\n\tpromisor = true\n'
                     "\tpartialclonefilter = blob:none\n")
        self.assertFails("partial_clone_unsupported")

    def test_promisor_pack_rejected(self):
        (self.git_dir / "objects" / "pack" / "pack-0.promisor").write_bytes(b"")
        self.assertFails("partial_clone_unsupported")

    def test_no_paid_service_or_dependency(self):
        for name in ("requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "package.json"):
            self.assertFalse((REPO_ROOT / name).exists(), name)


class T13Sha256Rejected(unittest.TestCase):
    def test_sha256_repository_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            try:
                repo = fx.Repo(Path(tmp) / "s256.git", object_format="sha256")
            except subprocess.CalledProcessError:
                self.skipTest("installed Git cannot create SHA-256 repositories")
            c = repo.commit(repo.tree({"a.txt": b"a\n"}), "s256\n")
            self.assertEqual(len(c), 64)
            for commit in (c, c[:40]):
                with self.subTest(commit=commit[:8]), self.assertRaises(inv.ScoutError) as cm:
                    inv.inventory(repo.git_dir, commit)
                self.assertEqual(cm.exception.code, "unsupported_object_format")


class T14Allowlist(Base):
    def test_actual_git_invocations_match_allowlist(self):
        log = self.root / "argv.log"
        wrapper = self.root / "logging-git"
        wrapper.write_text(f'#!/bin/sh\nfor a in "$@"; do printf "%s\\037" "$a"; done >> "{log}"\n'
                           f'printf "\\n" >> "{log}"\nexec "{fx.GIT}" "$@"\n')
        wrapper.chmod(0o755)
        m = self.scan(git_executable=str(wrapper))
        self.assertEqual(m["status"], "complete")
        calls = [tuple(line.split("\x1f")[:-1]) for line in log.read_text().splitlines()]
        prefix = (f"--git-dir={self.git_dir.resolve()}", *inv.GIT_GLOBAL_OPTIONS)
        c2 = self.f["c2"]
        self.assertEqual(calls, [
            (*prefix, "rev-parse", "--show-object-format=storage"),
            (*prefix, "cat-file", "-t", c2),
            (*prefix, "ls-tree", "-r", "-z", "-l", "--full-tree", c2),
        ])

    def test_runner_refuses_other_commands(self):
        runner = inv.GitRunner(fx.GIT, str(self.git_dir), inv.Limits())
        sha = self.f["c2"]
        for args in (("checkout", sha), ("cat-file", "-p", sha), ("cat-file", "-t", "HEAD"), ("ls-tree", sha),
                     ("fetch", "origin"), ("rev-parse", "HEAD"), ("ls-tree", "-r", "-z", "-l", "--full-tree", "main")):
            with self.subTest(args=args), self.assertRaises(inv.ScoutError) as cm:
                runner.run(*args)
            self.assertEqual(cm.exception.code, "command_not_allowed")
        self.assertEqual(runner.calls, [])

    def test_no_shell_and_fixed_argv(self):
        source = (PKG / "inventory.py").read_text()
        self.assertIn("shell=False", source)
        self.assertNotRegex(source, r"os\.system|shell=True|os\.popen")


class T15FailClosed(Base):
    def test_failure_replaces_stale_success(self):
        out = self.out / "m.json"
        ok = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out))
        self.assertEqual(ok.returncode, 0)
        self.assertEqual(json.loads(out.read_text())["status"], "complete")
        bad = cli("inventory", "--git-dir", str(self.git_dir), "--commit", "0" * 40, "--output", str(out))
        self.assertEqual(bad.returncode, 1)
        m = json.loads(out.read_text())
        self.assertEqual((m["status"], m["error"]["code"], m["entries"]), ("failed", "commit_not_found", []))
        self.assertNotIn("coverage", m)
        self.assertEqual([p.name for p in self.out.iterdir()], ["m.json"])

    def test_every_failure_code_writes_failed_manifest(self):
        cases = {
            "invalid_commit_id": ["--commit", "HEAD"],
            "entry_limit": ["--commit", self.f["c2"], "--max-entries", "2"],
            "output_limit": ["--commit", self.f["c2"], "--max-git-output-bytes", "10"],
            "not_a_git_dir": ["--commit", self.f["c2"], "--git-dir", str(self.root / "markers")],
        }
        for code, extra in cases.items():
            with self.subTest(code=code):
                out = self.out / f"{code}.json"
                args = ["inventory", "--git-dir", str(self.git_dir), "--output", str(out), *extra]
                r = cli(*args)
                self.assertEqual(r.returncode, 1, r.stderr)
                self.assertEqual(json.loads(out.read_text())["error"]["code"], code)

    def test_interrupted_write_keeps_previous_file_and_no_temp(self):
        out = self.out / "m.json"
        out.write_bytes(b"previous\n")
        with mock.patch("os.replace", side_effect=OSError("disk full")), self.assertRaises(OSError):
            inv.write_atomic(out, b"new\n")
        self.assertEqual(out.read_bytes(), b"previous\n")
        self.assertEqual([p.name for p in self.out.iterdir()], ["m.json"])

    def test_usage_errors_write_nothing(self):
        out = self.out / "m.json"
        for extra in (["--max-entries", "0"], ["--timeout", "-1"]):
            r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out), *extra)
            self.assertEqual(r.returncode, 2)
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"],
                "--output", str(self.root / "missing-dir" / "m.json"))
        self.assertEqual(r.returncode, 2)
        self.assertFalse(out.exists())

    def test_help(self):
        r = cli("inventory", "--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn(b"--commit", r.stdout)


if __name__ == "__main__":
    unittest.main()
