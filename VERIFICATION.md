# LF backport verification

The proposed flow worked in GitHub Actions on October 4, 2026.
[Run](https://github.com/flaviut/backport-demo/actions/runs/37222160568)
created [PR #4](https://github.com/flaviut/backport-demo/pull/4) without
conflicts. All six backported files contain 11 LF endings and zero CRLF.

The working configuration was introduced in
[commit 09bd98e](https://github.com/flaviut/backport-demo/commit/09bd98ea92e579b4be6c48bb7a149d150c3e4c69):
it enables `merge.renormalize=true` before the action and adds the byte-level
verification. The destination's LF policy and normalization were installed in
[commit d1e10b2](https://github.com/flaviut/backport-demo/commit/d1e10b246599ab4bde883dfde07d52bb61dc8064).
Both are needed for the tested flow.

The source was the original merged PR, whose files had CRLF, LF, and mixed
endings. The destination started at v1.0.0, then received this policy and a
separate normalization commit:

```gitattributes
*.py text eol=lf
```

```sh
git add .gitattributes
git add --renormalize src
git commit -m "Declare LF policy and normalize source"
```

Before running the backport action, the workflow enabled:

```sh
git config --local merge.renormalize true
```

The run used FreeCAD's pinned backport-action v4.5.2
(`66065406958f46e82238fd59546f5a99e69e22aa`) and Git 2.55.0.
It ran ordinary `git cherry-pick -x`, without whitespace-tolerant options.

The [verification workflow](.github/workflows/verify-renormalize.yml)
requires the action's success output and checks committed Git blobs.
Every blob must exactly equal the original PR's blob with CRLF converted
to LF, have 11 LF endings, and contain no CR bytes or conflict markers.
The same assertions passed locally after fetching the generated PR.

For comparison, the earlier LF destination without normalization attributes
had four conflicts; whitespace-tolerant picking succeeded but restored
CRLF and mixed endings. See the [earlier results](README.md#observed-results-2026-10-04).

For FreeCAD, install the source-file policy on each destination branch being
normalized and enable renormalization before its backport action.
Review deeper `.gitattributes` rules: `-text` overrides a root text policy.
This test covers the six fixtures, not FreeCAD's full tree or genuine
content conflicts. FreeCAD was not modified. PR #4 remains open for inspection.
