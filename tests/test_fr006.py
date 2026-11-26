"""FR-006 K-01/K-02 regressions, using only synthetic local Git fixtures."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from arc_scout import inventory as inv
from arc_scout import __main__ as cli


class FR006Regression(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git = shutil.which("git")
        if not self.git:
            self.skipTest("Git required")
        self.repo = self.root / "subject.git"
        self.git_call("init", "--bare", "--object-format=sha1", str(self.repo))
        tree = self.git_call(f"--git-dir={self.repo}", "mktree", data=b"").decode().strip()
        self.sha = self.git_call(f"--git-dir={self.repo}", "commit-tree", tree, "-m", "fixture").decode().strip()
        self.out = self.root / "manifest.json"
        self.rec = self.root / "run.json"
        self.target = self.root / "preserve.txt"
        self.target.write_bytes(b"external original\n")

    def git_call(self, *args, data=None):
        env = {"PATH": os.defpath, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
               "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
               "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
               "GIT_AUTHOR_DATE": "2000-01-01T00:00:00+00:00", "GIT_COMMITTER_DATE": "2000-01-01T00:00:00+00:00"}
        return subprocess.run([self.git, *args], env=env, input=data, capture_output=True, check=True).stdout

    def args(self, output=None, record=None, repo=None, extra=()):
        args = ["inventory", "--git-dir", str(repo or self.repo), "--commit", self.sha,
                "--output", str(output or self.out)]
        if record is not None:
            args += ["--run-record", str(record)]
        return args + list(extra)

    def refused(self, args):
        with mock.patch.object(inv, "write_atomic") as write, mock.patch.object(inv.subprocess, "Popen") as spawn, \
                mock.patch("sys.stderr"), self.assertRaises(SystemExit) as cm:
            cli.main(args)
        self.assertEqual(cm.exception.code, 2)
        write.assert_not_called()
        spawn.assert_not_called()

    def test_internal_symlink_destination_is_inside_subject(self):
        path = self.repo / "output.json"
        path.symlink_to(self.target)
        self.assertTrue(inv.output_inside_subject(path, self.repo))

    def test_internal_output_symlink_preserved(self):
        path = self.repo / "output.json"
        path.symlink_to(self.target)
        self.refused(self.args(output=path))
        self.assertTrue(path.is_symlink())
        self.assertEqual(path.readlink(), self.target)
        self.assertEqual(self.target.read_bytes(), b"external original\n")

    def test_internal_run_record_symlink_preserved(self):
        path = self.repo / "run.json"
        path.symlink_to(self.target)
        self.out.write_bytes(b"old output\n")
        self.refused(self.args(record=path))
        self.assertTrue(path.is_symlink())
        self.assertEqual(self.out.read_bytes(), b"old output\n")
        self.assertEqual(self.target.read_bytes(), b"external original\n")

    def test_external_symlinks_to_internal_external_or_missing_target_refused(self):
        for target in (self.repo / "config", self.target, self.root / "missing"):
            with self.subTest(target=target):
                before = target.read_bytes() if target.exists() else None
                path = self.root / "alias.json"
                path.symlink_to(target)
                self.refused(self.args(output=path))
                self.refused(self.args(record=path))
                self.assertTrue(path.is_symlink())
                self.assertEqual(target.read_bytes() if target.exists() else None, before)
                path.unlink()

    def test_parent_symlink_into_subject_refused(self):
        alias = self.root / "alias-dir"
        alias.symlink_to(self.repo, target_is_directory=True)
        self.refused(self.args(output=alias / "new.json"))
        self.refused(self.args(record=alias / "new.json"))
        self.assertFalse((self.repo / "new.json").exists())

    def test_ordinary_worktree_is_protected(self):
        work = self.root / "work"
        self.git_call("init", str(work))
        path = work / "keep.txt"
        path.write_bytes(b"worktree original\n")
        self.refused(self.args(output=path, repo=work / ".git"))
        self.refused(self.args(record=path, repo=work / ".git"))
        self.assertEqual(path.read_bytes(), b"worktree original\n")

    def test_ambiguous_worktree_layout_refused_before_writes(self):
        work = self.root / "external-worktree"
        work.mkdir()
        keep = work / "keep.txt"
        keep.write_bytes(b"worktree original\n")
        with (self.repo / "config").open("a") as stream:
            stream.write(f"\n[core]\n\tworktree = {work}\n")
        self.refused(self.args(output=keep))
        self.refused(self.args(record=keep))
        self.assertEqual(keep.read_bytes(), b"worktree original\n")
        with self.assertRaises(inv.ScoutError) as cm:
            inv.inventory(self.repo, self.sha)
        self.assertEqual(cm.exception.code, "unsupported_layout")

    def test_gitfile_and_git_directory_symlink_refused(self):
        work = self.root / "linked-work"
        work.mkdir()
        gitfile = work / ".git"
        gitfile.write_text(f"gitdir: {self.repo}\n")
        alias = self.root / "alias.git"
        alias.symlink_to(self.repo, target_is_directory=True)
        for path in (gitfile, alias):
            with self.subTest(path=path):
                self.refused(self.args(repo=path))
                self.refused(self.args(repo=path, record=self.repo / "config"))
        self.assertFalse(self.out.exists())
        self.assertTrue(alias.is_symlink())

    def test_nonbare_non_dot_git_layout_refused(self):
        self.git_call(f"--git-dir={self.repo}", "config", "core.bare", "false")
        self.refused(self.args())
        with self.assertRaises(inv.ScoutError) as cm:
            inv.inventory(self.repo, self.sha)
        self.assertEqual(cm.exception.code, "unsupported_layout")

    def test_nonfinite_and_oversized_cli_timeout_refused(self):
        self.out.write_bytes(b"old manifest\n")
        for value in ("nan", "inf", "-inf", "1e300", "3601", "0", "-1"):
            with self.subTest(value=value):
                self.refused(self.args(extra=(f"--timeout={value}",)))
        self.assertEqual(self.out.read_bytes(), b"old manifest\n")

    def test_callable_and_runner_invalid_limits_never_spawn(self):
        for key, values in {"timeout_seconds": [float("nan"), float("inf"), -float("inf"), 1e300, 3601, 0, True, "1"],
                            "max_entries": [0, -1, 1.5, True, inv.DEFAULT_MAX_ENTRIES + 1],
                            "max_path_bytes": [0, inv.DEFAULT_MAX_PATH_BYTES + 1],
                            "max_component_bytes": [0, inv.DEFAULT_MAX_COMPONENT_BYTES + 1],
                            "max_git_output_bytes": [0, inv.DEFAULT_MAX_GIT_OUTPUT_BYTES + 1]}.items():
            for value in values:
                with self.subTest(key=key, value=value), mock.patch.object(inv.subprocess, "Popen") as spawn:
                    limits = replace(inv.Limits(), **{key: value})
                    with self.assertRaises(inv.ScoutError) as cm:
                        inv.inventory(self.repo, self.sha, limits=limits)
                    self.assertEqual(cm.exception.code, "invalid_limits")
                    runner = inv.GitRunner(self.git, str(self.repo), limits)
                    with self.assertRaises(inv.ScoutError) as cm:
                        runner.run("rev-parse", "--show-object-format=storage")
                    self.assertEqual(cm.exception.code, "invalid_limits")
                    spawn.assert_not_called()

    def test_unexpected_collection_error_and_interrupt_reap_real_child(self):
        fake_git = self.root / "slow-git"
        fake_git.write_text("#!/bin/sh\nexec sleep 30\n")
        fake_git.chmod(0o755)
        for exc in (ValueError("collection error"), KeyboardInterrupt()):
            children = []
            def fail(proc, sub):
                children.append(proc)
                raise exc
            runner = inv.GitRunner(str(fake_git), str(self.repo), inv.Limits(timeout_seconds=1))
            try:
                with self.subTest(exc=type(exc).__name__), mock.patch.object(runner, "_collect", side_effect=fail):
                    with self.assertRaises(type(exc)):
                        runner.run("rev-parse", "--show-object-format=storage")
                    self.assertEqual(len(children), 1)
                    self.assertIsNotNone(children[0].poll(), "collector failed but child survived")
                    self.assertTrue(children[0].stdout.closed)
                    self.assertTrue(children[0].stderr.closed)
            finally:
                for proc in children:
                    if proc.poll() is None:
                        proc.kill()
                        proc.wait(timeout=5)

    def test_normal_scan_and_failed_scan_preserve_contract(self):
        self.assertEqual(cli.main(self.args(record=self.rec, extra=("--timeout=10",))), 0)
        original = self.out.read_bytes()
        self.assertEqual(json.loads(original)["status"], "complete")
        self.assertEqual(json.loads(self.rec.read_bytes())["status"], "complete")
        self.assertEqual(cli.main(self.args()), 0)
        self.assertEqual(self.out.read_bytes(), original)
        with mock.patch("sys.stderr"):
            self.assertEqual(cli.main(self.args(extra=("--commit", "HEAD"))), 1)
        self.assertEqual(json.loads(self.out.read_bytes())["status"], "failed")


if __name__ == "__main__":
    unittest.main()
