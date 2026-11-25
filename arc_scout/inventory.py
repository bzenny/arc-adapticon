"""Deterministic, metadata-only inventory of a local Git commit.

Scout runs exactly three read-only Git plumbing commands (see ALLOWED_COMMANDS)
against an explicit local Git directory. It never checks out, reads file
contents into its own logic, follows symlinks or gitlinks, or runs repository
code. Trust boundary: trusted, self-contained local fixtures on POSIX; this is
not a sandbox for hostile repositories and not a network-isolation guarantee.
"""

from __future__ import annotations

import json
import os
import re
import select
import shutil
import signal
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

SCHEMA_VERSION = "0.1.0"
TOOL_VERSION = "0.1.0"  # keep equal to arc_scout.__version__

DEFAULT_MAX_ENTRIES = 100_000
DEFAULT_MAX_PATH_BYTES = 4096
DEFAULT_MAX_COMPONENT_BYTES = 255
DEFAULT_MAX_GIT_OUTPUT_BYTES = 64 * 1024 * 1024
DEFAULT_TIMEOUT_SECONDS = 60.0
MAX_STDERR_BYTES = 64 * 1024

FULL_SHA1 = re.compile(r"[0-9a-f]{40}")

# Global options placed before every subcommand. They pin configuration that
# could otherwise reach the network, prompt for credentials or run programs.
GIT_GLOBAL_OPTIONS = (
    "--no-replace-objects",
    "-c", "protocol.allow=never",
    "-c", "protocol.file.allow=never",
    "-c", "protocol.git.allow=never",
    "-c", "protocol.ssh.allow=never",
    "-c", "protocol.http.allow=never",
    "-c", "protocol.https.allow=never",
    "-c", "protocol.ext.allow=never",
    "-c", "credential.helper=",
    "-c", "core.fsmonitor=false",
    "-c", "core.hooksPath=/dev/null",
    "-c", "core.askPass=",
)

# The only subcommands Scout may run; "<sha>" is a validated 40-hex commit ID.
ALLOWED_COMMANDS = (
    ("rev-parse", "--show-object-format=storage"),
    ("cat-file", "-t", "<sha>"),
    ("ls-tree", "-r", "-z", "-l", "--full-tree", "<sha>"),
)

LIMITATIONS = (
    "Metadata only: file contents are not read into Scout and are not assessed.",
    "Symlinks and gitlinks are listed but never followed; submodule contents are not inspected.",
    "Git reads objects internally to report blob sizes; Scout does not claim zero object access.",
    "Trust boundary: trusted, self-contained local Git directories on POSIX; not a sandbox for hostile repositories.",
    "Only SHA-1 object storage is supported in schema 0.1.0.",
    "License, dependency and runtime assessments are not performed.",
)

OMISSION_REASONS = (
    "symlink_not_followed",
    "gitlink_not_followed",
    "unsafe_path",
    "path_not_utf8",
    "path_too_long",
    "unsupported_mode",
)

_TEXT_MODES = {"100644": "regular", "100755": "executable"}


class ScoutError(Exception):
    """A scan failure with a stable machine-readable code."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class Limits:
    max_entries: int = DEFAULT_MAX_ENTRIES
    max_path_bytes: int = DEFAULT_MAX_PATH_BYTES
    max_component_bytes: int = DEFAULT_MAX_COMPONENT_BYTES
    max_git_output_bytes: int = DEFAULT_MAX_GIT_OUTPUT_BYTES
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS


@dataclass
class GitRunner:
    """Runs allowlisted Git commands with a sanitized environment."""

    git_executable: str
    git_dir: str
    limits: Limits
    calls: list[tuple[str, ...]] = field(default_factory=list)

    def env(self) -> dict[str, str]:
        return sanitized_environment()

    def run(self, *args: str) -> bytes:
        check_allowed(args)
        argv = [self.git_executable, f"--git-dir={self.git_dir}", *GIT_GLOBAL_OPTIONS, *args]
        self.calls.append(tuple(args))
        try:
            proc = subprocess.Popen(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.env(),
                cwd=os.path.abspath(os.sep),
                close_fds=True,
                start_new_session=True,
                shell=False,
            )
        except FileNotFoundError:
            raise ScoutError("git_not_found", "Git executable not found") from None
        except PermissionError:
            raise ScoutError("git_not_found", "Git executable is not runnable") from None

        try:
            out, err, code = self._collect(proc, args[0])
        finally:
            for pipe in (proc.stdout, proc.stderr):
                try:
                    pipe.close()
                except OSError:
                    pass
        if code != 0:
            raise _GitFailure(args[0], code, bytes(err))
        return bytes(out)

    def _collect(self, proc: subprocess.Popen, sub: str) -> tuple[bytes, bytes, int]:
        """Read both pipes until EOF and reap Git, all within one absolute deadline.

        A descendant that keeps a pipe open after Git exits cannot extend the
        deadline: at expiry the whole process group is killed and Scout stops
        reading, whether or not the descendant has exited.
        """
        deadline = time.monotonic() + self.limits.timeout_seconds
        cap = self.limits.max_git_output_bytes
        out, err = bytearray(), bytearray()
        fds = {proc.stdout.fileno(): out, proc.stderr.fileno(): err}
        for fd in fds:
            os.set_blocking(fd, False)
        while fds:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                _terminate(proc)
                raise ScoutError("timeout", f"git {sub} exceeded {self.limits.timeout_seconds} s")
            ready, _, _ = select.select(list(fds), [], [], remaining)
            for fd in ready:
                try:
                    chunk = os.read(fd, 65536)
                except BlockingIOError:
                    continue
                if not chunk:
                    del fds[fd]
                    continue
                buf = fds[fd]
                if buf is out:
                    if len(out) + len(chunk) > cap:
                        _terminate(proc)
                        raise ScoutError("output_limit", f"git {sub} output exceeded {cap} bytes")
                    out.extend(chunk)
                elif len(err) < MAX_STDERR_BYTES:
                    err.extend(chunk[: MAX_STDERR_BYTES - len(err)])
        try:
            code = proc.wait(timeout=max(deadline - time.monotonic(), 0.001))
        except subprocess.TimeoutExpired:
            _terminate(proc)
            raise ScoutError("timeout", f"git {sub} exceeded {self.limits.timeout_seconds} s") from None
        return bytes(out), bytes(err), code


def _terminate(proc: subprocess.Popen) -> None:
    """Kill Git's process group and reap Git without waiting indefinitely."""
    _kill_group(proc)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


def _kill_group(proc: subprocess.Popen) -> None:
    """Kill the Git process and any children it started (own session)."""
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        proc.kill()


class _GitFailure(ScoutError):
    def __init__(self, sub: str, code: int, stderr: bytes):
        super().__init__("git_failed", f"git {sub} exited {code}")
        self.stderr = stderr.decode("utf-8", "replace")


def sanitized_environment() -> dict[str, str]:
    """A fixed environment; nothing is inherited from the caller."""
    return {
        "PATH": os.defpath,
        "LC_ALL": "C",
        "LANG": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "XDG_CONFIG_HOME": os.devnull,
        "GIT_ATTR_NOSYSTEM": "1",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PROTOCOL_FROM_USER": "0",
    }


def check_allowed(args: tuple[str, ...]) -> None:
    for pattern in ALLOWED_COMMANDS:
        if len(pattern) == len(args) and all(
            p == a or (p == "<sha>" and FULL_SHA1.fullmatch(a)) for p, a in zip(pattern, args)
        ):
            return
    raise ScoutError("command_not_allowed", f"git command not in allowlist: {args[:1]}")


def find_git(git_executable: str | None) -> str:
    if git_executable is None:
        found = shutil.which("git")
        if found is None:
            raise ScoutError("git_not_found", "Git executable not found on PATH")
        return found
    if not os.path.isfile(git_executable) or not os.access(git_executable, os.X_OK):
        raise ScoutError("git_not_found", "Git executable not found")
    return git_executable


def resolve_git_dir(git_dir: str | os.PathLike) -> Path:
    path = Path(git_dir)
    if not path.is_dir():
        raise ScoutError("not_a_git_dir", "Git directory does not exist")
    return path.resolve()


_SECTION = re.compile(r'\[\s*([A-Za-z0-9.-]+)(?:\s+"((?:[^"\\]|\\.)*)")?\s*\](.*)')
_KEY = re.compile(r"([A-Za-z][A-Za-z0-9-]*)\s*(?:=(.*))?")


def parse_git_config(data: bytes) -> list[tuple[str, str | None, str, str | None]]:
    """Parse Git config text into (section, subsection, key, raw value) tuples.

    Deliberately small and strict: anything it cannot parse is rejected rather
    than guessed. Section and key names are lower-cased; ``[a.b]`` gives
    subsection ``b``.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise ScoutError("config_unsupported", "subject config is not UTF-8") from None
    lines = text.splitlines()
    items: list[tuple[str, str | None, str, str | None]] = []
    section: tuple[str, str | None] | None = None
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        while line.endswith("\\") and i + 1 < len(lines):  # value continuation
            i += 1
            line = line[:-1] + lines[i].strip()
        i += 1
        if not line or line[0] in "#;":
            continue
        if line.startswith("["):
            m = _SECTION.fullmatch(line)
            if m is None:
                raise ScoutError("config_unsupported", "unparseable section header in subject config")
            name, sub, rest = m.group(1).lower(), m.group(2), m.group(3).strip()
            if sub is None and "." in name:
                name, sub = name.split(".", 1)
            section = (name, sub)
            if not rest or rest[0] in "#;":
                continue
            line = rest
        if section is None:
            raise ScoutError("config_unsupported", "subject config has a key outside any section")
        m = _KEY.fullmatch(line)
        if m is None:
            raise ScoutError("config_unsupported", "unparseable line in subject config")
        items.append((section[0], section[1], m.group(1).lower(), m.group(2)))
    return items


def check_config(items: list[tuple[str, str | None, str, str | None]]) -> None:
    """Reject configuration outside the trusted-fixture profile."""
    for section, sub, key, _ in items:
        if section in ("include", "includeif"):
            raise ScoutError("config_include_unsupported", "subject config uses include or includeIf")
        if (section == "extensions" and key == "partialclone") or key in ("promisor", "partialclonefilter"):
            raise ScoutError("partial_clone_unsupported", "partial-clone or promisor configuration present")
        if section == "extensions" and key != "objectformat":
            raise ScoutError("config_unsupported", f"repository extension not supported: {key}")
        if section == "protocol":
            raise ScoutError("config_unsupported", "subject config sets protocol policy")


def check_layout(git_dir: Path) -> None:
    """Accept only a self-contained bare repository or a non-linked ``.git`` directory."""
    if not (git_dir / "HEAD").is_file():
        raise ScoutError("not_a_git_dir", "no HEAD file; not a Git directory")
    if (git_dir / "commondir").exists() or (git_dir / "config.worktree").exists():
        raise ScoutError("unsupported_layout", "linked worktree or per-worktree config is not supported")
    if not (git_dir / "objects").is_dir():
        raise ScoutError("not_a_git_dir", "no objects directory; not a Git directory")
    if (git_dir / "objects").is_symlink():
        raise ScoutError("unsupported_layout", "objects directory is a symlink")
    info = git_dir / "objects" / "info"
    for name in ("alternates", "http-alternates"):
        if (info / name).exists():
            raise ScoutError("alternates_unsupported", "alternate object stores are not supported")
    pack = git_dir / "objects" / "pack"
    if pack.is_dir() and any(p.suffix == ".promisor" for p in pack.iterdir()):
        raise ScoutError("partial_clone_unsupported", "promisor packs present; partial clones are not supported")
    config = git_dir / "config"
    if config.is_symlink() or not config.is_file():
        raise ScoutError("unsupported_layout", "config missing or a symlink")
    check_config(parse_git_config(config.read_bytes()))


def output_inside_subject(output: Path, git_dir: Path) -> bool:
    out = output.resolve()
    roots = [git_dir]
    if git_dir.name == ".git":
        roots.append(git_dir.parent)
    return any(out == r or r in out.parents for r in roots)


def classify_path(raw: bytes, limits: Limits) -> tuple[str | None, str | None]:
    """Return (decoded path or None, omission reason or None)."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "path_not_utf8"
    if len(raw) > limits.max_path_bytes:
        return text, "path_too_long"
    if raw.startswith(b"/") or b"\\" in raw or b":" in raw or any(b < 0x20 or b == 0x7F for b in raw):
        return text, "unsafe_path"
    for part in raw.split(b"/"):
        if part in (b"", b".", b"..") or part.lower() == b".git":
            return text, "unsafe_path"
        if len(part) > limits.max_component_bytes:
            return text, "path_too_long"
    return text, None


_RECORD = re.compile(rb"([0-7]{6}) (blob|tree|commit) ([0-9a-f]{40}) +(-|BAD|[0-9]+)\t(.*)", re.S)


def parse_ls_tree(data: bytes, limits: Limits) -> list[dict]:
    if data and not data.endswith(b"\0"):
        raise ScoutError("malformed_git_output", "ls-tree output is not NUL-terminated")
    records = data.split(b"\0")[:-1] if data else []
    if len(records) > limits.max_entries:
        raise ScoutError("entry_limit", f"tree has more than {limits.max_entries} entries")
    entries = []
    for rec in records:
        m = _RECORD.fullmatch(rec)
        if m is None:
            raise ScoutError("malformed_git_output", "unparseable ls-tree record")
        mode, otype, oid, size, raw_path = (g.decode("ascii") if i < 4 else g for i, g in enumerate(m.groups()))
        if size == "BAD":  # Git could not read the object to size it
            raise ScoutError("missing_object", "a tree entry refers to a missing object")
        path, reason = classify_path(raw_path, limits)
        if reason is None:
            if mode == "120000":
                reason = "symlink_not_followed"
            elif mode == "160000" or otype == "commit":
                reason = "gitlink_not_followed"
            elif mode not in _TEXT_MODES or otype != "blob":
                reason = "unsupported_mode"
        if reason is None and size == "-":
            raise ScoutError("malformed_git_output", "blob entry without a size")
        entry = {
            "path": path,
            "mode": mode,
            "type": otype,
            "object_id": oid,
            "size_bytes": None if size == "-" else int(size),
            "disposition": "omitted" if reason else "included",
        }
        if path is None:
            entry["path_hex"] = raw_path.hex()
        if reason:
            entry["omission_reason"] = reason
        entries.append((raw_path, entry))
    raw_paths = [raw for raw, _ in entries]
    seen = set(raw_paths)
    if len(seen) != len(raw_paths):
        raise ScoutError("malformed_tree", "tree lists the same path more than once")
    for raw in raw_paths:
        parts = raw.split(b"/")
        for k in range(1, len(parts)):
            if b"/".join(parts[:k]) in seen:
                raise ScoutError("malformed_tree", "tree lists a path as both a file and a directory")
    entries.sort(key=lambda e: e[0])
    return [e for _, e in entries]


def inventory(
    git_dir: str | os.PathLike,
    commit: str,
    *,
    git_executable: str | None = None,
    limits: Limits = Limits(),
    runner_factory=GitRunner,
) -> dict:
    """Return the canonical manifest for ``commit`` or raise ScoutError."""
    if os.name != "posix":
        raise ScoutError("unsupported_platform", "Scout P004 supports POSIX systems only")
    git = find_git(git_executable)
    gdir = resolve_git_dir(git_dir)
    check_layout(gdir)  # before any Git call: Git reads the subject config itself
    runner = runner_factory(git, str(gdir), limits)

    try:
        fmt = runner.run("rev-parse", "--show-object-format=storage").decode("ascii", "replace").strip()
    except _GitFailure:
        raise ScoutError("not_a_git_dir", "not a readable Git directory") from None
    if fmt == "sha256":
        raise ScoutError("unsupported_object_format", "SHA-256 repositories are not supported in schema 0.1.0")
    if fmt != "sha1":
        raise ScoutError("unsupported_object_format", "unrecognized object format")

    if not isinstance(commit, str) or not FULL_SHA1.fullmatch(commit):
        raise ScoutError("invalid_commit_id", "commit must be a full 40-character lowercase hexadecimal SHA-1")

    try:
        otype = runner.run("cat-file", "-t", commit).decode("ascii", "replace").strip()
    except _GitFailure:
        raise ScoutError("commit_not_found", "commit object not found") from None
    if otype != "commit":
        raise ScoutError("not_a_commit", f"object is a {otype}, not a commit")

    try:
        listing = runner.run("ls-tree", "-r", "-z", "-l", "--full-tree", commit)
    except _GitFailure as exc:
        raise ScoutError("missing_object", "tree listing failed; objects may be missing") from exc
    entries = parse_ls_tree(listing, limits)
    return build_manifest(commit, fmt, entries, limits)


def build_manifest(commit: str, fmt: str, entries: list[dict], limits: Limits) -> dict:
    included = [e for e in entries if e["disposition"] == "included"]
    omissions = []
    for e in entries:
        if e["disposition"] == "omitted":
            o = {"path": e["path"], "reason": e["omission_reason"]}
            if "path_hex" in e:
                o["path_hex"] = e["path_hex"]
            omissions.append(o)
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "arc-scout", "version": TOOL_VERSION},
        "status": "complete",
        "subject": {"commit": commit, "object_format": fmt},
        "policy": {
            "max_path_bytes": limits.max_path_bytes,
            "max_component_bytes": limits.max_component_bytes,
        },
        "coverage": {
            "tree_entries": len(entries),
            "included": len(included),
            "omitted": len(omissions),
            "included_bytes": sum(e["size_bytes"] for e in included),
        },
        "entries": entries,
        "omissions": omissions,
        "assessment": {"license": "unknown", "dependencies": "unknown", "runtime": "not_verified"},
        "limitations": list(LIMITATIONS),
    }


def failure_manifest(code: str, message: str, commit: str | None, status: str = "failed") -> dict:
    """A non-result manifest: ``failed`` after a scan error, ``incomplete`` while a scan runs."""
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "arc-scout", "version": TOOL_VERSION},
        "status": status,
        "error": {"code": code, "message": message},
        "subject": {"commit": commit if isinstance(commit, str) and FULL_SHA1.fullmatch(commit) else None},
        "entries": [],
        "omissions": [],
        "assessment": {"license": "unknown", "dependencies": "unknown", "runtime": "not_verified"},
        "limitations": list(LIMITATIONS),
    }


def serialize(manifest: dict) -> bytes:
    return (json.dumps(manifest, sort_keys=True, ensure_ascii=True, indent=2) + "\n").encode("ascii")


def write_atomic(path: Path, data: bytes) -> None:
    """Write via a temporary file in the same directory, then rename over ``path``."""
    directory = path.parent
    fd, tmp = tempfile.mkstemp(prefix=".arc-scout-", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
