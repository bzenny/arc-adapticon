"""Command line: ``python -m arc_scout inventory --git-dir D --commit SHA --output F``.

Exit status (callers must check it; only exit 0 with ``status: complete`` is a result):
  0  complete manifest written
  1  scan failed: a ``status: failed`` manifest replaced the output
  2  usage or preflight refusal: nothing written, an existing output is untouched
  3  output could not be written: the output was invalidated (``status: incomplete``)
     or removed where possible; any remaining file must not be used
Before a valid scan starts, the output is atomically replaced with a
``status: incomplete`` manifest, so an earlier success cannot survive an
interrupted or failed run.
"""

from __future__ import annotations

import argparse
import datetime
import platform
import sys
import traceback
from pathlib import Path

from . import inventory as inv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m arc_scout",
        description="ARC Scout: deterministic, metadata-only inventory of a local Git commit. "
        "Never checks out, reads file contents, follows links or runs repository code.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("inventory", help="write a JSON inventory manifest for one commit")
    p.add_argument("--git-dir", required=True, help="local Git directory (bare repository or .git)")
    p.add_argument("--commit", required=True, help="full 40-character lowercase SHA-1 commit ID")
    p.add_argument("--output", required=True, help="manifest path, outside the subject repository")
    p.add_argument("--run-record", help="optional separate run record (timestamps, environment)")
    p.add_argument("--git", dest="git_executable", help="Git executable (default: git on PATH)")
    p.add_argument("--max-entries", type=int, default=inv.DEFAULT_MAX_ENTRIES)
    p.add_argument("--max-path-bytes", type=int, default=inv.DEFAULT_MAX_PATH_BYTES)
    p.add_argument("--max-git-output-bytes", type=int, default=inv.DEFAULT_MAX_GIT_OUTPUT_BYTES)
    p.add_argument("--timeout", type=float, default=inv.DEFAULT_TIMEOUT_SECONDS, help="seconds per Git command")
    return parser


def _check_destination(parser: argparse.ArgumentParser, label: str, path: Path, git_dir: Path) -> None:
    if not path.parent.is_dir():
        parser.error(f"{label}: directory does not exist: {path.parent}")
    if path.is_dir():
        parser.error(f"{label}: is a directory: {path}")
    if git_dir.is_dir() and inv.output_inside_subject(path, git_dir.resolve()):
        parser.error(f"{label}: must be outside the subject repository")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    for name in ("max_entries", "max_path_bytes", "max_git_output_bytes"):
        if getattr(args, name) < 1:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    output = Path(args.output)
    git_dir = Path(args.git_dir)
    _check_destination(parser, "--output", output, git_dir)
    run_record = Path(args.run_record) if args.run_record else None
    if run_record is not None:
        _check_destination(parser, "--run-record", run_record, git_dir)
        if run_record.resolve() == output.resolve():
            parser.error("--run-record must differ from --output")

    limits = inv.Limits(
        max_entries=args.max_entries,
        max_path_bytes=args.max_path_bytes,
        max_git_output_bytes=args.max_git_output_bytes,
        timeout_seconds=args.timeout,
    )
    started = datetime.datetime.now(datetime.timezone.utc)
    pending = inv.serialize(inv.failure_manifest(
        "scan_in_progress", "scan started and has not finished; this is not a result", args.commit,
        status="incomplete"))
    for target in (output, run_record):
        if target is None:
            continue
        try:
            inv.write_atomic(target, pending)
        except OSError as exc:
            removed = _remove_stale(target)
            print(f"arc-scout: error [output_unwritable]: cannot invalidate {target}: {exc.strerror or exc}; "
                  f"earlier file {'removed' if removed else 'NOT removed and must not be used'}", file=sys.stderr)
            return 3

    try:
        manifest = inv.inventory(git_dir, args.commit, git_executable=args.git_executable, limits=limits)
        code = 0
    except inv.ScoutError as exc:
        manifest = inv.failure_manifest(exc.code, exc.message, args.commit)
        print(f"arc-scout: error [{exc.code}]: {exc.message}", file=sys.stderr)
        code = 1
    except Exception:  # fail closed on anything unexpected
        traceback.print_exc()
        manifest = inv.failure_manifest("internal_error", "unexpected internal error", args.commit)
        code = 1
    try:
        inv.write_atomic(output, inv.serialize(manifest))
    except OSError as exc:
        print(f"arc-scout: error [output_unwritable]: cannot write {output}: {exc.strerror or exc}; "
              "it still holds the status: incomplete placeholder", file=sys.stderr)
        return 3

    if run_record is not None:
        record = {
            "record": "arc-scout run record (not part of the canonical manifest)",
            "tool_version": inv.TOOL_VERSION,
            "started_at": started.isoformat(),
            "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": manifest["status"],
            "exit_code": code,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "git_dir": str(git_dir.resolve()),
            "output": str(output.resolve()),
            "limits": vars(limits),
        }
        try:
            inv.write_atomic(run_record, inv.serialize(record))
        except OSError as exc:
            print(f"arc-scout: error [output_unwritable]: cannot write run record: {exc.strerror or exc}",
                  file=sys.stderr)
            return 3
    return code


def _remove_stale(path: Path) -> bool:
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return True
    except OSError:
        return False


if __name__ == "__main__":
    sys.exit(main())
