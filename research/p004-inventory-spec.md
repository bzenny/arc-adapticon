# P004 — ARC Scout local inventory (M1 step 1)

Status: candidate implementation (PUSH 004), prepared by Claude; requires independent review by an agent that did not prepare it and separate founder merge authorization. Scope source: [FR-004](reviews/FR-004-push-003-review.md) P004 scope and addendum refinements; authorization ARC-EVO-0051. Stage 2 (Inventory) of the [Scout protocol](scout-protocol.md) for trusted local fixtures only.

## Interface

```
python -m arc_scout inventory --git-dir ./fixture.git --commit <40-hex SHA-1> --output ./manifest.json
    [--run-record ./run.json] [--git PATH] [--max-entries N] [--max-path-bytes N]
    [--max-git-output-bytes N] [--timeout SECONDS]
```

Exit 0: complete manifest written. Exit 1: scan failed; a `status: failed` manifest with `error.code` atomically replaces the output, so a stale success cannot remain. Exit 2: usage error; nothing written (includes an output inside the subject Git directory, or inside the worktree of a `.git` directory).

## Trust boundary and security limits

Trusted local synthetic fixtures. P004 is **not** a sandbox for arbitrary hostile repositories: Git itself parses the subject's objects, packs and local config. Passing T09 and T10 shows that this metadata slice does not read repository text into Scout and does not run repository code; it does not show resistance to prompt injection in later content extraction, model interpretation or im-ICM generation, which need their own adversarial tests.

## Order of checks

1. Locate Git (`--git` or PATH); missing → `git_not_found`.
2. `--git-dir` must be an existing directory → else `not_a_git_dir`.
3. `rev-parse --show-object-format=storage`: failure → `not_a_git_dir`; `sha256` or other → `unsupported_object_format`.
4. Reject partial clones: `*.promisor` packs or `partialclone`/`promisor` in the subject config → `partial_clone_unsupported` (Python file read; no Git command).
5. Commit argument must match `[0-9a-f]{40}` exactly → else `invalid_commit_id` (no branch, tag, abbreviation, uppercase or revision expression).
6. `cat-file -t <sha>`: failure → `commit_not_found`; type other than `commit` → `not_a_commit`.
7. `ls-tree -r -z -l --full-tree <sha>`: failure or a `BAD` size → `missing_object`; unparseable → `malformed_git_output`; more than `max_entries` records → `entry_limit`.

Any Git call exceeding `--timeout` → `timeout` (process group killed); stdout over `--max-git-output-bytes` → `output_limit`.

## Authorized Git commands

Each call is a fixed argument array, no shell, `stdin` closed, own session, `cwd=/`:

```
git --git-dir=<abs> --no-replace-objects -c protocol.allow=never -c credential.helper= \
    -c core.fsmonitor=false -c core.hooksPath=/dev/null -c core.askPass= <subcommand>
  rev-parse --show-object-format=storage
  cat-file -t <sha>
  ls-tree -r -z -l --full-tree <sha>
```

The runner refuses anything else (`command_not_allowed`). Environment is built from scratch, nothing inherited: `PATH=os.defpath`, `LC_ALL=LANG=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=XDG_CONFIG_HOME=/dev/null`, `GIT_ATTR_NOSYSTEM=1`, `GIT_NO_REPLACE_OBJECTS=1`, `GIT_NO_LAZY_FETCH=1` (honoured by Git 2.44+; on older Git, `protocol.allow=never` and the partial-clone rejection keep the scan offline), `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0`, `GIT_PROTOCOL_FROM_USER=0`. Git reads objects internally to report blob sizes; Scout never receives file contents.

## Entry policy

| Condition | Disposition | `omission_reason` |
|---|---|---|
| Mode 100644 or 100755 blob, safe path | included | — |
| Mode 120000 (symlink) | omitted, never followed; `size_bytes` is the link-target length Git reports | `symlink_not_followed` |
| Mode 160000 (gitlink/submodule) | omitted, never inspected; `size_bytes` null | `gitlink_not_followed` |
| Path not UTF-8 | omitted; `path` null, `path_hex` gives the bytes | `path_not_utf8` |
| Leading `/`, backslash, control byte, empty, `.` or `..` component, `.git` component (any case) | omitted | `unsafe_path` |
| Path over `max_path_bytes` (4096) or component over 255 bytes | omitted | `path_too_long` |
| Any other mode | omitted | `unsupported_mode` |

## Manifest contract (schema 0.1.0)

Top-level keys: `schema_version`, `tool` {name, version}, `status` (`complete` or `failed`), `subject` {commit, object_format}, `policy` {max_path_bytes, max_component_bytes}, `coverage` {tree_entries, included, omitted, included_bytes}, `entries`, `omissions`, `assessment` {license: unknown, dependencies: unknown, runtime: not_verified}, `limitations`. Each entry: `path`, `mode`, `type`, `object_id`, `size_bytes`, `disposition`, plus `omission_reason` and `path_hex` where applicable. `omissions` repeats each omitted path with its reason. A failed manifest has `status: failed`, `error` {code, message}, empty `entries` and `omissions`, no `coverage`, and `subject.commit` only if the argument was a well-formed SHA.

Determinism: entries sorted by raw path bytes; JSON with sorted keys, two-space indent, ASCII escapes, trailing newline. No timestamps, absolute paths or environment data in the manifest; those go only in the optional `--run-record`. Same input and tool version give byte-identical output (T02).

Atomic output: a temporary file in the output directory, fsync, then `os.replace`; on error the temporary file is removed and any earlier file is left whole.

## Acceptance tests

| ID | Requirement | Test class |
|---|---|---|
| T01 | Exact inventory equals an expectation built independently (blob IDs computed in Python) | `T01ExactInventory` |
| T02 | Repeated runs, other cwd and hostile caller environment: byte-identical; no timestamps or absolute paths | `T02Deterministic` |
| T03 | Pinned older commit inventoried; its commit ID recomputed from raw object formats | `T03HistoricalCommit` |
| T04 | Branch, HEAD, abbreviations, uppercase, expressions, nonexistent, blob, tree, tag, missing object, non-repository rejected | `T04InvalidCommits` |
| T05 | Missing Git: explicit, absent from PATH, and through the CLI | `T05MissingGit` |
| T06 | `..`, `.git`, `.GIT`, backslash, control byte, non-UTF-8, `.` and over-long paths omitted with reasons | `T06UnsafePaths` |
| T07 | Symlinks (including to `/etc/passwd`) and a gitlink to an absent commit omitted, not followed | `T07LinksNotFollowed` |
| T08 | Entry, output-size, path-length and timeout limits | `T08Limits` |
| T09 | Instruction-bearing README: not echoed, not acted on, no markers | `T09HostileReadme` |
| T10 | `run.sh`, `setup.py`, `Makefile`, npm `postinstall`, five Git hooks and a configured fsmonitor never run; control test shows canaries are live | `T10Canaries` |
| T11 | Subject Git directory byte-identical (mode, size, mtime, SHA-256) after successful and failed scans; output inside subject refused | `T11SubjectUnchanged` |
| T12 | No network modules imported; environment not inherited; partial clones rejected; no dependency manifests | `T12Offline` |
| T13 | SHA-256 repository rejected as `unsupported_object_format` | `T13Sha256Rejected` |
| T14 | Real argv captured by a logging Git wrapper equals the allowlist exactly; other commands refused | `T14Allowlist` |
| T15 | Failure replaces an earlier success; every failure code writes a failed manifest; interrupted write keeps the old file; usage errors write nothing | `T15FailClosed` |

These are slice-level checks. They do not complete Scout S-1 to S-8 or ARC-EXP-001.

## Not in scope

Remote acquisition (P005), adapters (P006, D-005: no installation or execution), content extraction, System Map or im-ICM projection (P007), evidence matrix (P008), weighted ranking (blocked by F-02), execution (M3, F-03).

## Rollback

Close the draft PR; main is unchanged. After merge, a reviewed revert plus a superseding ledger event. No data, settings or dependencies to remove.
