# P004 — ARC Scout local inventory (M1 step 1)

Status: candidate implementation (PUSH 004 and 004.1 prepared by Claude; bounded PUSH 004.2 amendment prepared by ChatGPT). [FR-006](reviews/FR-006-p004-review.md) requested corrections K-01 and K-02 at the earlier head. The amended head requires independent reassessment by an agent that did not prepare the amendment, with prior review provenance retained, and separate exact-head founder merge authorization. Scope source: [FR-004](reviews/FR-004-push-003-review.md) P004 scope and addendum refinements; authorization ARC-EVO-0051. Corrections: [P004 preliminary review](reviews/P004-preliminary-review.md) items 1 to 3. Stage 2 (Inventory) of the [Scout protocol](scout-protocol.md), for trusted local fixtures only.

## Interface

```
python -m arc_scout inventory --git-dir ./fixture.git --commit <40-hex SHA-1> --output ./manifest.json
    [--run-record ./run.json] [--git PATH] [--max-entries N] [--max-path-bytes N]
    [--max-git-output-bytes N] [--timeout SECONDS]
```

| Exit | Meaning | Output file afterwards |
|---|---|---|
| 0 | Complete | `status: complete` manifest |
| 1 | Scan failed | `status: failed` manifest with `error.code` |
| 2 | Usage or preflight refusal | Nothing written; any existing file untouched |
| 3 | Output or run record could not be written | `status: incomplete` placeholder or removed where possible; an old file may remain if invalidation and removal both fail. If the optional run-record final write fails, a current complete manifest may exist, but the invocation is unsuccessful. Always check exit status and stderr. |

Only exit 0 with `status: complete` is a result. Callers must check the exit status.

**Invalidation before scanning.** After argument and destination checks pass (exit 2 otherwise), Scout atomically replaces the output, and the run record if one was requested, with a `status: incomplete` manifest (`error.code: scan_in_progress`). Only then does it scan, and it finishes by atomically writing `complete` or `failed`. A run that is killed, interrupted or fails to write its final result therefore leaves `incomplete`, never an earlier success (T15b). If the placeholder cannot be written, Scout tries to remove the old file and exits 3.

Preflight refusals (exit 2; no output writes, removals or Git invocations):
- either output parent is missing, final destination is a symlink (including dangling links), or existing destination is not a regular file
- either destination's actual directory entry (resolved parent plus leaf) or dereferenced target is inside the supplied or resolved subject Git directory or ordinary `.git` worktree
- run record equal to the output
- symlinked Git directory, gitfile, or a recognizable Git-like directory failing the layout/config checks below; ordinary missing or empty non-repository input can still produce a failed manifest outside the subject
- invalid or excessive limits; see bounds below

This preflight protects both manifest and run record before either is touched. It assumes a trusted, stable filesystem and is not resistant to concurrent hostile path replacement.

## Supported platforms and fixture layouts

**Platforms.** POSIX only. Tested on Linux with Python 3.12.3 and 3.13.18, and Git 2.43.0. Process-group termination (`killpg`) and pipe polling (`select`) are POSIX facilities. Any other platform gets `unsupported_platform`. macOS is expected to work but has not been tested.

**Trusted local fixture layouts.** Two layouts are supported:
- a self-contained bare repository
- the `.git` directory of a non-linked repository

Each must contain a `HEAD` file, a real `objects` directory (not a symlink) and a regular `config` file. Require exactly one explicit ordinary `core.bare = true` or `false` (unquoted, case-insensitive, optional comments); `false` is supported only for an ordinary `.git` directory. Explicit `core.worktree`, nonstandard non-bare Git directories, linked layouts and a final Git-directory symlink are refused instead of guessing a subject root. These are refused:

| Condition | Code |
|---|---|
| `.git` is a file (gitfile, linked worktree, submodule), or `HEAD` or `objects` missing | `not_a_git_dir` |
| `commondir` or `config.worktree` present, Git directory/`objects`/`config` is a symlink, `config` missing, ambiguous `core.bare` or explicit `core.worktree`, non-bare directory not named `.git` | `unsupported_layout` |
| `objects/info/alternates` or `objects/info/http-alternates` present | `alternates_unsupported` |
| `*.promisor` pack present | `partial_clone_unsupported` |

**Subject config.** It is read with a small, strict parser covering sections, subsections, comments, inline keys and continuations. Anything the parser cannot read is refused. These checks run before the first Git command, because Git itself reads this file.

| Config | Code |
|---|---|
| `include` or `includeIf` section, any case | `config_include_unsupported` |
| `extensions.partialClone`, or any `promisor` or `partialCloneFilter` key | `partial_clone_unsupported` |
| Any `extensions` key other than `objectFormat` | `config_unsupported` |
| Any `protocol` section | `config_unsupported` |
| Unparseable line, non-UTF-8, key outside a section | `config_unsupported` |

Other keys are allowed and are pinned by the global options below where they could matter. P004.2 performs these checks before writing output for recognizable Git layouts; the callable API retains its stable ScoutError codes, while CLI preflight refusal exits 2 without writing.

## Trust boundary and security limits

P004 is **not** a sandbox for arbitrary hostile repositories, and it does not claim comprehensive network isolation:
- Git still parses the subject's objects, packs and allowed config. The layout and config rules narrow what Git reads; they do not make hostile input safe.
- Offline behaviour rests on three things: `protocol.allow=never` plus every per-protocol override set to `never`; rejection of promisor, partial-clone and alternates configuration; and `GIT_NO_LAZY_FETCH=1`. The last is honoured only by Git 2.44 and later; the test machine runs 2.43.0.
- The test suite also passes inside a network namespace with no network. That shows these tests need no network. It is not a proof that Git can never open one.

T09 and T10 show that this metadata slice does not read repository text into Scout and does not run repository code. They do not show resistance to prompt injection in later content extraction, model interpretation or im-ICM generation. Those stages need their own adversarial tests, and any future materialization of files needs its own path and link tests.

## Order of checks

0. Validate all Limits values before subprocess launch; failure → `invalid_limits` in the callable API or exit 2 at CLI preflight.
1. Platform must be POSIX → else `unsupported_platform`.
2. Locate Git (`--git` or `PATH`) → missing gives `git_not_found`.
3. `--git-dir` must be an existing directory → else `not_a_git_dir`.
4. Layout and subject-config rules above (Python file reads; no Git command yet).
5. `rev-parse --show-object-format=storage`:
   - failure → `not_a_git_dir`
   - `sha256` or anything else → `unsupported_object_format`
6. Commit argument must match `[0-9a-f]{40}` exactly → else `invalid_commit_id`. No branch, tag, abbreviation, uppercase or revision expression.
7. `cat-file -t <sha>`:
   - failure → `commit_not_found`
   - type other than `commit` → `not_a_commit`
8. `ls-tree -r -z -l --full-tree <sha>`:
   - failure, or a `BAD` size → `missing_object`
   - unparseable output → `malformed_git_output`
   - more than `max_entries` records → `entry_limit`
   - a path listed twice, or as both a file and a directory → `malformed_tree`

## Process bounds

Each Git call runs in its own session. Scout reads stdout and stderr in a single-threaded `select` loop against one absolute deadline (`--timeout`). Both CLI and callable inventory/runner validate limits before spawning: timeout finite and positive, at most 3,600 seconds; integer entries/path bytes/component bytes/Git stdout bytes in 1..100,000 / 4,096 / 255 / 67,108,864 respectively. Boolean and non-integer values are not accepted as integer limits. The integer ceilings deliberately retain the previous default maxima.

- When the deadline passes, or stdout exceeds `--max-git-output-bytes`, Scout kills the whole process group. It then reaps Git, waiting at most 5 s, and returns `timeout` or `output_limit`.
- Unexpected collection exceptions and interrupts take the same bounded termination/reaping path before re-raising; pipes close in the finally block. A descendant that keeps a pipe open after Git exits cannot extend the deadline (T08b).
- A descendant that left Git's session is not killed, but Scout stops reading and returns on time. stderr is capped at 64 KiB.

## Authorized Git commands

Each call is a fixed argument array with no shell, `stdin` closed, its own session, and `cwd=/`:

```
git --git-dir=<abs> --no-replace-objects -c protocol.allow=never \
    -c protocol.file.allow=never -c protocol.git.allow=never -c protocol.ssh.allow=never \
    -c protocol.http.allow=never -c protocol.https.allow=never -c protocol.ext.allow=never \
    -c credential.helper= -c core.fsmonitor=false -c core.hooksPath=/dev/null -c core.askPass= <subcommand>
  rev-parse --show-object-format=storage
  cat-file -t <sha>
  ls-tree -r -z -l --full-tree <sha>
```

The runner refuses anything else (`command_not_allowed`).

The environment is built from scratch; nothing is inherited:

| Variable | Value |
|---|---|
| `PATH` | `os.defpath` |
| `LC_ALL`, `LANG` | `C` |
| `GIT_CONFIG_NOSYSTEM` | `1` |
| `GIT_CONFIG_GLOBAL`, `XDG_CONFIG_HOME` | `/dev/null` |
| `GIT_ATTR_NOSYSTEM`, `GIT_NO_REPLACE_OBJECTS`, `GIT_NO_LAZY_FETCH` | `1` |
| `GIT_TERMINAL_PROMPT`, `GIT_OPTIONAL_LOCKS`, `GIT_PROTOCOL_FROM_USER` | `0` |

Git reads objects internally to report blob sizes; Scout never receives file contents.

## Entry policy

| Condition | Disposition | `omission_reason` |
|---|---|---|
| Mode 100644 or 100755 blob, safe path | included | — |
| Mode 120000 (symlink) | omitted, never followed; `size_bytes` is the link-target length Git reports | `symlink_not_followed` |
| Mode 160000 (gitlink/submodule) | omitted, never inspected; `size_bytes` null | `gitlink_not_followed` |
| Path not UTF-8 | omitted; `path` null, `path_hex` gives the bytes | `path_not_utf8` |
| Unsafe path (any condition listed below) | omitted | `unsafe_path` |
| Path over `max_path_bytes` (4096) or component over 255 bytes | omitted | `path_too_long` |
| Any other mode | omitted | `unsupported_mode` |

A path counts as unsafe if it has any of these:
- a leading `/`
- a backslash
- a colon (covers drive-qualified `C:`, `C:/` and NTFS stream names)
- a control byte
- an empty, `.` or `..` component
- a `.git` component, in any case

Windows reserved device names and trailing-dot names are not checked. Scout materializes no files.

## Manifest contract (schema 0.1.0)

Top-level keys:

| Key | Content |
|---|---|
| `schema_version` | `0.1.0` |
| `tool` | name, version |
| `status` | `complete`, `failed` or `incomplete` |
| `subject` | commit, object_format |
| `policy` | max_path_bytes, max_component_bytes |
| `coverage` | tree_entries, included, omitted, included_bytes |
| `entries` | one per tree entry |
| `omissions` | each omitted path again, with its reason |
| `assessment` | license `unknown`, dependencies `unknown`, runtime `not_verified` |
| `limitations` | fixed list |

Each entry has `path`, `mode`, `type`, `object_id`, `size_bytes` and `disposition`, plus `omission_reason` and `path_hex` where they apply.

`failed` and `incomplete` manifests carry `error` {code, message}. Their `entries` and `omissions` are empty and they have no `coverage`. `subject.commit` is present only if the argument was a well-formed SHA.

**Determinism.** Entries are sorted by raw path bytes. JSON uses sorted keys, two-space indent, ASCII escapes and a trailing newline. The manifest holds no timestamps, absolute paths or environment data; those go only in the optional `--run-record`. The same input and tool version give byte-identical output (T02).

**Atomic writes.** Scout writes a temporary file in the output directory, fsyncs it, then calls `os.replace`. On error the temporary file is removed and any earlier file is left whole. After successful pre-scan invalidation, a failed scan write leaves the incomplete placeholder rather than an earlier success. Preflight refusal, storage failure, or an optional run-record final-write failure are governed by the exit table; callers must check the exit code.

## Acceptance tests

`python -m unittest discover -s tests -v`: 79 tests (original 66 unchanged plus 13 P004.2 regressions).

| ID | Requirement | Test class |
|---|---|---|
| T01 | Exact inventory equals an expectation built independently (blob IDs computed in Python) | `T01ExactInventory` |
| T02 | Repeated runs, other cwd and hostile caller environment give byte-identical output; no timestamps or absolute paths | `T02Deterministic` |
| T03 | Pinned older commit inventoried; its commit ID recomputed from raw object formats | `T03HistoricalCommit` |
| T04 | Rejects branch, HEAD, abbreviations, uppercase and revision expressions; nonexistent, blob, tree and tag objects; missing objects; a non-repository | `T04InvalidCommits` |
| T05 | Missing Git: explicit path, absent from PATH, and through the CLI | `T05MissingGit` |
| T06 | `..`, `.git`, `.GIT`, backslash, control byte, non-UTF-8, `.` and over-long paths omitted with reasons | `T06UnsafePaths` |
| T06b | Duplicate entries and file/directory conflicts rejected; drive-qualified and stream paths omitted | `T06bMalformedTrees` |
| T07 | Symlinks (including to `/etc/passwd`) and a gitlink to an absent commit omitted, not followed | `T07LinksNotFollowed` |
| T08 | Entry, output-size, path-length and timeout limits | `T08Limits` |
| T08b | Descendants holding stdout or stderr after Git exits are killed within the deadline; a session-escaped descendant cannot extend it; flooding output is cut off; non-POSIX refused | `T08bProcessTermination` |
| T09 | Instruction-bearing README: not echoed, not acted on, no markers | `T09HostileReadme` |
| T10 | `run.sh`, `setup.py`, `Makefile`, npm `postinstall`, five Git hooks and a configured fsmonitor never run; a control test shows the canaries are live | `T10Canaries` |
| T11 | Subject Git directory byte-identical (mode, size, mtime, SHA-256) after successful and failed scans; output inside the subject refused | `T11SubjectUnchanged` |
| T12 | No network modules imported; environment not inherited; partial clones rejected; no dependency manifests | `T12Offline` |
| T12b | Includes rejected before any Git call; partial-clone, protocol and extension config rejected; unparseable config rejected; benign syntax accepted; alternates, linked layouts, symlinked objects, gitfiles and headless dirs rejected | `T12bFixtureBoundary` |
| T13 | SHA-256 repository rejected as `unsupported_object_format` | `T13Sha256Rejected` |
| T14 | Real argv captured by a logging Git wrapper equals the allowlist exactly; other commands refused | `T14Allowlist` |
| T15 | Failure replaces an earlier success; every failure code writes a failed manifest; an interrupted write keeps the old file; usage errors write nothing | `T15FailClosed` |
| T15b | A run killed mid-scan leaves `incomplete`; a failed final write leaves `incomplete` and exits 3; a failed placeholder removes the stale success; an unwritable directory exits 3; preflight refusal leaves the output untouched; the run record is invalidated too | `T15bInvalidation` |
| K-01 / K-02 | Internal/external/dangling output and run-record symlinks, symlinked parent, ordinary and ambiguous worktrees, gitfiles, non-bare non-.git layouts, invalid finite bounds at CLI/API/runner, real-child cleanup after unexpected collector failure and KeyboardInterrupt, normal manifest contract | `FR006Regression` in [test_fr006.py](../tests/test_fr006.py) |

`T15b.test_unwritable_directory_reports_exit_3` skips when run as root, because root ignores directory permissions. Run the suite as an unprivileged user to exercise it.

### P004.2 implementer verification (not independent review)

Python 3.13.5, Git 2.47.3, Linux. Reconstructed original runtime and original 66-test/fixture files from the exact 76e746b GitHub blobs; all original Python blob IDs verified before editing. `python -W error::ResourceWarning -m unittest discover -s tests -v`: 79 tests, 78 passed, one root-only skip, zero failures/errors. Ran the skipped permission case separately as `nobody`: pass. Repeated the entire suite in a network namespace (`unshare -rn`) in two batches (39 and 40 tests), same one root-only skip, zero failures/errors; a probe to a documentation-range address returned ENETUNREACH (errno 101). Running `runuser` inside that namespace was not permitted; the separate unprivileged test ran outside it. Source/test blobs in the candidate must match the locally tested bytes: inventory.py d55e0eb6a35027f00c658f8cfdf77c518ba1ea4a; __main__.py 92e46afef6790b8cb53d84a8295b839dbe206cb9; test_fr006.py 65ea42bc4e7706fbac7fd5372e10d05d68345174. Original tests/test_inventory.py 009df61f90cfc797c62afd21898adf1b5a112fa8 and tests/fixtures.py 55955273d2871375dc7b640c0e0d2ceb9de9f04f remain unchanged. No live remote acquisition, hostile-repo sandbox, macOS or Windows validation is claimed.

These are slice-level checks. They do not complete Scout S-1 to S-8 or ARC-EXP-001.

## Not in scope

| Item | Where it belongs |
|---|---|
| Remote acquisition | P005 |
| Adapters | P006; under D-005, no installation or execution |
| Content extraction, System Map or im-ICM projection | P007 |
| Evidence matrix | P008 |
| Weighted ranking | Blocked by F-02 |
| Execution | M3, blocked by F-03 |

## Rollback

Close the draft PR; main is unchanged. After merge, roll back with a reviewed revert plus a superseding ledger event. There are no data, settings or dependencies to remove.
