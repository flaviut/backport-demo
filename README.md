# Backport line ending experiment

See [FreeCAD backport LF verification](VERIFICATION.md) for a controlled
before-and-after test of the minimal patch to FreeCAD's current workflow.

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
