# FreeCAD backport LF verification

The minimal workflow patch worked. On October 4, 2026, the same source PR
and LF release destination failed before the patch and succeeded afterward.

The [baseline commit](https://github.com/flaviut/backport-demo/commit/e32ee49e8838ea24852fe85ba1756bdfd4533c35)
uses FreeCAD's current backport workflow, including its pinned actions,
triggers, checkout ref, and backport inputs. Its only adaptation is replacing
FreeCAD's private CI secret with the demo's built-in GitHub token.

The [fix commit](https://github.com/flaviut/backport-demo/commit/5e679d228ced6cec99d5f73561b1d575b845c3e7)
changes only `.github/workflows/backport.yml`, inserting these three lines
between checkout and the existing backport action:

```yaml
      - name: Normalize historical line endings during backports
        run: git config --local merge.renormalize true

```

No test workflow, action upgrade, or verification script is part of that fix.
A dry-run `git apply --check` confirmed it applies directly to
`../FreeCAD/.github/workflows/backport.yml`; FreeCAD was not modified.

Prerequisite: the
[destination preparation commit](https://github.com/flaviut/backport-demo/commit/2c49c5b08e2d6b7a499a374ba2924f1b316b4ac4)
declares `*.py text eol=lf` and normalizes the fixtures with
`git add --renormalize src`. This policy was present in both runs.
The workflow patch alone does not establish an LF policy.

| Same source and destination | Observed result |
| --- | --- |
| [Before the fix](https://github.com/flaviut/backport-demo/actions/runs/37223225137) | Four content conflicts in CRLF/mixed fixtures; no backport PR. |
| [After the fix](https://github.com/flaviut/backport-demo/actions/runs/37223279605) | [PR #5](https://github.com/flaviut/backport-demo/pull/5), no conflicts; all six files entirely LF. |

Both runs used ordinary `git cherry-pick -x`. The fetched PR #5 blobs passed
[byte-level assertions](scripts/verify-lf-backport.py): exactly the original
PR content with CRLF converted to LF, 11 LF endings per file, zero CR bytes,
and no conflict markers. Recheck with:

```sh
git fetch origin
python3 scripts/verify-lf-backport.py origin/backport-1-to-releases/FreeCAD-LF-proof f96751f9316f99aab61cb27d0c817113c7fc2fcb
```

The failed control still had a green workflow status; its logs and PR comment
record the failure. These results cover six fixtures, not FreeCAD's full
tree. FreeCAD's deeper `-text` attributes must be reviewed when establishing
its LF policy. Earlier demo history is preserved on `archive/prior-verification`.
