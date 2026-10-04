# Backport line ending experiment

Six Python fixtures: two CRLF, two LF, and two alternating CRLF/LF.
Git autocrlf is disabled and no attributes normalize the fixtures.

The initial release is tagged v1.0.0 with branch release-1.0.
An original PR changes VALUE and adds a source line in every fixture while
preserving each fixture's existing ending style. After merging, main is
converted to LF. Labels trigger korthout/backport-action with default settings.

release-1.0 retains the tagged release's endings. A second target,
release-1.0-lf, contains only an LF normalization commit above that release.
This separates normalization on main from normalization on the destination.

Inspect committed bytes with:

```sh
python3 scripts/audit-endings.py v1.0.0 main release-1.0 release-1.0-lf
```

## Observed results (2026-10-04)

Repository: https://github.com/flaviut/backport-demo (private).
Original PR: https://github.com/flaviut/backport-demo/pull/1, squash merged as
`f96751f9316f99aab61cb27d0c817113c7fc2fcb`. Main's subsequent LF normalization
is commit `c702794`. No `.gitattributes` or merge renormalization was configured.
The action resolved to `8560fb503c275d433c56f05a2f64850093baa9f7` (v4),
with Git 2.55.0 on the GitHub runner.

| Destination and mode | Outcome |
| --- | --- |
| Original release endings, default | PR #2 created without conflicts; every source blob matches the original merged PR exactly. |
| LF-normalized release, default | Content conflicts in both CRLF and both mixed fixtures; no PR created. |
| LF-normalized release, whitespace_tolerant | PR #3 created without conflicts; CRLF and mixed endings returned to the destination. |

Both successful backports contain these counts per file (each row applies
to two fixtures):

| Fixture category | CRLF | LF |
| --- | ---: | ---: |
| CRLF | 11 | 0 |
| LF | 0 | 11 |
| Mixed | 6 | 5 |

Main remains entirely LF: 11 LF endings per source file, zero CRLF.
The normalized target was entirely LF before PR #3. The tolerant cherry-pick
therefore reintroduces inconsistent endings across files and mixed endings
within the mixed files. Its logs show `git cherry-pick -x -Xignore-space-at-eol`;
this option tolerates ending differences but does not enforce LF output.

Evidence:

- Original backport: https://github.com/flaviut/backport-demo/pull/2
- Default conflict run: https://github.com/flaviut/backport-demo/actions/runs/37220281856
- Tolerant backport: https://github.com/flaviut/backport-demo/pull/3
- Tolerant run: https://github.com/flaviut/backport-demo/actions/runs/37220433539

The default conflict run has a green workflow status despite the failed
backport. The action comments on the original PR and reports unsuccessful
backports through its outputs; a successful workflow alone is insufficient.
Both backport PRs are left open for inspection.

Normalization on main does not alter the original PR's historical commit.
The action cherry-picks that commit, so main's later normalization is absent
from either backport. These observations apply to the tested fixtures and
configuration, not every possible Git merge or attributes configuration.

The initial original-target label was applied before main's normalization
push completed (a local push-remote configuration caused the first push to
fail). After explicitly pushing to origin/main, the label was removed and
reapplied; the action retained the already-created PR #2. The normalized
target runs both occurred after the normalization was pushed.

To reproduce the byte audit of the actual remote PR heads:

```sh
git fetch origin
python3 scripts/audit-endings.py origin/main origin/backport-1-to-release-1.0 origin/backport-1-to-release-1.0-lf
```

Label events use the default merge mode. Manually dispatching the workflow
runs the whitespace-tolerant comparison for PR #1 against release-1.0-lf.
