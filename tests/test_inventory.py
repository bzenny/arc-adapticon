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


# --- PUSH 004.1 regression tests (FR-005 / P004 preliminary review items 1-4) ---


class T06bMalformedTrees(Base):
    def test_duplicate_entries_rejected(self):
        repo = self.f["repo"]
        a, b = repo.blob(b"one\n"), repo.blob(b"two\n")
        tree = repo.raw_tree([("100644", b"dup.txt", a), ("100644", b"dup.txt", b), ("100644", b"ok", a)])
        self.assertFails("malformed_tree", repo.commit(tree, "dup\n"))

    def test_file_and_directory_with_same_path_rejected(self):
        repo = self.f["repo"]
        sub = repo.tree({"x": b"x\n"})
        tree = repo.raw_tree([("100644", b"a", repo.blob(b"a\n")), ("40000", b"a", sub)])
        self.assertFails("malformed_tree", repo.commit(tree, "conflict\n"))

    def test_drive_qualified_and_stream_paths_omitted(self):
        repo = self.f["repo"]
        spec = {"C:evil.txt": b"x\n", "D:": {"x.txt": b"x\n"}, "notes.txt:stream": b"x\n", "fine.txt": b"x\n"}
        m = self.scan(repo.commit(repo.tree(spec), "drive\n"))
        by = {e["path"]: e for e in m["entries"]}
        for p in ("C:evil.txt", "D:/x.txt", "notes.txt:stream"):
            with self.subTest(path=p):
                self.assertEqual(by[p]["omission_reason"], "unsafe_path")
        self.assertEqual(by["fine.txt"]["disposition"], "included")

    def test_classify_drive_forms(self):
        for raw in (b"C:/x", b"c:x", b"a/b:c", b"Z:"):
            with self.subTest(raw=raw):
                self.assertEqual(inv.classify_path(raw, inv.Limits())[1], "unsafe_path")


def _alive(pid: int) -> bool:
    try:
        with open(f"/proc/{pid}/stat") as fh:
            return fh.read().rsplit(")", 1)[1].split()[0] != "Z"
    except FileNotFoundError:
        return False
    except OSError:
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False


class T08bProcessTermination(Base):
    def _fake_git(self, body: str) -> Path:
        path = self.root / "fake-git"
        path.write_text("#!/bin/sh\n" + body)
        path.chmod(0o755)
        return path

    def _timed(self, git: Path, limit: float = 1.0) -> float:
        import time
        t0 = time.monotonic()
        self.assertFails("timeout", git_executable=str(git), limits=inv.Limits(timeout_seconds=limit))
        return time.monotonic() - t0

    def _pid(self) -> int:
        import time
        f = self.root / "pid"
        for _ in range(100):
            if f.exists() and f.read_text().strip():
                return int(f.read_text())
            time.sleep(0.05)
        self.fail("descendant pid not written")

    def _wait_dead(self, pid: int) -> bool:
        import time
        for _ in range(50):
            if not _alive(pid):
                return True
            time.sleep(0.05)
        return False

    def test_descendant_holding_stdout_after_leader_exits(self):
        git = self._fake_git(f'sleep 30 &\necho $! > "{self.root / "pid"}"\nexit 0\n')
        self.assertLess(self._timed(git), 4)
        self.assertTrue(self._wait_dead(self._pid()), "descendant in Git's process group survived")

    def test_descendant_holding_only_stderr(self):
        git = self._fake_git(f'sleep 30 >/dev/null &\necho $! > "{self.root / "pid"}"\nexit 0\n')
        self.assertLess(self._timed(git), 4)
        self.assertTrue(self._wait_dead(self._pid()))

    def test_escaped_descendant_cannot_extend_deadline(self):
        # A descendant that leaves Git's session is out of reach of killpg; Scout still returns on time.
        code = "import os,time; os.setsid(); time.sleep(30)"
        git = self._fake_git(f'"{sys.executable}" -c "{code}" &\necho $! > "{self.root / "pid"}"\nexit 0\n')
        try:
            self.assertLess(self._timed(git), 4)
        finally:
            try:
                os.kill(self._pid(), 9)
            except ProcessLookupError:
                pass

    def test_flooding_output_is_cut_off(self):
        git = self._fake_git("exec yes\n")
        self.assertFails("output_limit", git_executable=str(git), limits=inv.Limits(max_git_output_bytes=1 << 16))

    def test_non_posix_refused(self):
        with mock.patch.object(inv.os, "name", "nt"):
            self.assertFails("unsupported_platform")


class T12bFixtureBoundary(Base):
    def _config(self, text: str) -> None:
        with open(self.git_dir / "config", "a") as fh:
            fh.write(text)

    def _logged_scan_fails(self, code: str) -> None:
        log = self.root / "argv.log"
        wrapper = self.root / "logging-git"
        wrapper.write_text(f'#!/bin/sh\necho "$@" >> "{log}"\nexec "{fx.GIT}" "$@"\n')
        wrapper.chmod(0o755)
        self.assertFails(code, git_executable=str(wrapper))
        self.assertFalse(log.exists(), "Git ran before the subject config was checked")

    def test_includes_rejected_before_any_git_call(self):
        canary = self.root / "inc.cfg"
        canary.write_text(f"[core]\n\tfsmonitor = {self.root / 'nope'}\n")
        for text in (f"[include]\n\tpath = {canary}\n", f'[includeIf "gitdir:/"]\n\tpath = {canary}\n',
                     f"[INCLUDE]\n\tpath = {canary}\n"):
            with self.subTest(text=text.splitlines()[0]):
                original = (self.git_dir / "config").read_text()
                self._config(text)
                self._logged_scan_fails("config_include_unsupported")
                (self.git_dir / "config").write_text(original)

    def test_partial_clone_configuration_variants(self):
        for text in ('[Remote "o"]\n\tPromisor = true\n', "[core]\n\tpartialCloneFilter = blob:none\n",
                     "[extensions]\n\tpartialClone = o\n", '[remote "o"] partialclonefilter = blob:none\n'):
            with self.subTest(text=text):
                original = (self.git_dir / "config").read_text()
                self._config(text)
                self.assertFails("partial_clone_unsupported")
                (self.git_dir / "config").write_text(original)

    def test_protocol_overrides_and_extensions_rejected(self):
        for text in ("[protocol]\n\tallow = always\n", '[protocol "file"]\n\tallow = always\n',
                     "[protocol.ext]\n\tallow = always\n", "[extensions]\n\tworktreeConfig = true\n"):
            with self.subTest(text=text):
                original = (self.git_dir / "config").read_text()
                self._config(text)
                self.assertFails("config_unsupported")
                (self.git_dir / "config").write_text(original)
        for proto in ("file", "git", "ssh", "http", "https", "ext"):
            self.assertIn(f"protocol.{proto}.allow=never", inv.GIT_GLOBAL_OPTIONS)

    def test_unparseable_config_rejected(self):
        for text in ("this is [not valid\n", "[core\n", "[core] = x\n"):
            with self.subTest(text=text):
                original = (self.git_dir / "config").read_text()
                self._config(text)
                self.assertFails("config_unsupported")
                (self.git_dir / "config").write_text(original)
        (self.git_dir / "config").write_text("bare = true\n")
        self.assertFails("config_unsupported")

    def test_benign_config_syntax_accepted(self):
        self._config('# comment\n; comment\n[remote "origin"]\n\turl = https://example.invalid/r.git # note\n'
                     '[branch.main]\n\tremote = origin\n[user] name = "A # B"\n[alias]\n\tx = !echo \\\n  hi\n')
        self.assertEqual(self.scan()["status"], "complete")

    def test_alternate_object_stores_rejected(self):
        info = self.git_dir / "objects" / "info"
        info.mkdir(exist_ok=True)
        for name in ("alternates", "http-alternates"):
            with self.subTest(name=name):
                (info / name).write_text(str(self.root) + "\n")
                self._logged_scan_fails("alternates_unsupported")
                (info / name).unlink()

    def test_linked_and_shared_layouts_rejected(self):
        for name in ("commondir", "config.worktree"):
            with self.subTest(name=name):
                (self.git_dir / name).write_text("..\n")
                self.assertFails("unsupported_layout")
                (self.git_dir / name).unlink()

    def test_objects_symlink_rejected(self):
        real = self.root / "real-objects"
        (self.git_dir / "objects").rename(real)
        (self.git_dir / "objects").symlink_to(real)
        self.assertFails("unsupported_layout")

    def test_gitfile_and_headless_dirs_rejected(self):
        work = self.root / "linked"
        work.mkdir()
        (work / ".git").write_text(f"gitdir: {self.git_dir}\n")
        with self.assertRaises(inv.ScoutError) as cm:
            inv.inventory(work / ".git", self.f["c2"])
        self.assertEqual(cm.exception.code, "not_a_git_dir")
        (self.git_dir / "HEAD").unlink()
        self.assertFails("not_a_git_dir")


class T15bInvalidation(Base):
    def _complete(self, out: Path) -> None:
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(out.read_text())["status"], "complete")

    def test_interrupted_run_leaves_incomplete_not_stale_success(self):
        import signal
        import time
        out = self.out / "m.json"
        self._complete(out)
        slow = self.root / "slow-git"
        slow.write_text(f'#!/bin/sh\nsleep 2\nexec "{fx.GIT}" "$@"\n')
        slow.chmod(0o755)
        base = {"PATH": os.environ.get("PATH", os.defpath), "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPATH": str(REPO_ROOT)}
        proc = subprocess.Popen([sys.executable, "-m", "arc_scout", "inventory", "--git-dir", str(self.git_dir),
                                 "--commit", self.f["c2"], "--output", str(out), "--git", str(slow)],
                                cwd=REPO_ROOT, env=base, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(200):
                if json.loads(out.read_text())["status"] == "incomplete":
                    break
                time.sleep(0.02)
            proc.send_signal(signal.SIGKILL)
            proc.wait(timeout=10)
        finally:
            if proc.poll() is None:
                proc.kill()
        m = json.loads(out.read_text())
        self.assertEqual((m["status"], m["error"]["code"]), ("incomplete", "scan_in_progress"))
        self.assertEqual(m["entries"], [])
        self.assertEqual([p.name for p in self.out.iterdir()], ["m.json"])

    def test_final_write_failure_keeps_placeholder_and_exits_3(self):
        import arc_scout.__main__ as cli_mod
        out = self.out / "m.json"
        self._complete(out)
        real = inv.write_atomic
        calls = []

        def flaky(path, data):
            calls.append(path)
            if len(calls) > 1:
                raise OSError(28, "No space left on device")
            real(path, data)

        with mock.patch.object(inv, "write_atomic", flaky), mock.patch("sys.stderr"):
            code = cli_mod.main(["inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"],
                                 "--output", str(out)])
        self.assertEqual(code, 3)
        self.assertEqual(json.loads(out.read_text())["status"], "incomplete")

    def test_preflight_write_failure_removes_stale_success(self):
        import arc_scout.__main__ as cli_mod
        out = self.out / "m.json"
        self._complete(out)
        with mock.patch.object(inv, "write_atomic", side_effect=OSError(13, "Permission denied")), \
                mock.patch("sys.stderr"):
            code = cli_mod.main(["inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"],
                                 "--output", str(out)])
        self.assertEqual(code, 3)
        self.assertFalse(out.exists())

    def test_unwritable_directory_reports_exit_3(self):
        if os.geteuid() == 0:
            self.skipTest("root ignores directory permissions")
        locked = self.root / "locked"
        locked.mkdir()
        locked.chmod(0o500)
        try:
            r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"],
                    "--output", str(locked / "m.json"))
        finally:
            locked.chmod(0o700)
        self.assertEqual(r.returncode, 3)
        self.assertIn(b"output_unwritable", r.stderr)

    def test_preflight_refusal_leaves_existing_output_untouched(self):
        out = self.out / "m.json"
        self._complete(out)
        before = out.read_bytes()
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", self.f["c2"], "--output", str(out),
                "--max-entries", "0")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(out.read_bytes(), before)

    def test_run_record_is_invalidated_too(self):
        out, rec = self.out / "m.json", self.out / "run.json"
        rec.write_text('{"status": "complete"}\n')
        r = cli("inventory", "--git-dir", str(self.git_dir), "--commit", "0" * 40, "--output", str(out),
                "--run-record", str(rec))
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(rec.read_text())["status"], "failed")


if __name__ == "__main__":
    unittest.main()
