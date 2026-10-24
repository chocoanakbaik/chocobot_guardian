# Chocobot Guardian — Release Checklist

Current status: **NOT READY FOR SALE** until all mandatory checks have evidence.

## Automated checks
- [ ] Python source compiles on Windows.
- [ ] Utility tests pass on Windows and Ubuntu.
- [ ] PyInstaller build succeeds from the same source revision.
- [ ] Packaged executable completes `--self-test` without opening the full GUI.
- [ ] Bundle includes logo, language packs, and required runtime assets.
- [ ] No secrets, private user files, or test artifacts are bundled.

## Manual Windows checks
- [ ] Install and first launch on a clean Windows 10/11 x64 device.
- [ ] Verify layout at common screen sizes and display scaling.
- [ ] Verify the app creates configuration/log folders under `%LOCALAPPDATA%\ChocobotGuardian`, not the installation directory.
- [ ] Change settings and language; restart and verify persistence.
- [ ] Test URL input validation for normal, malformed, punycode, IP-literal and user-info URLs.
- [ ] Verify file information, SHA-256, folder inventory and file-analysis outputs on sample files.
- [ ] Verify folder analysis handles inaccessible items and the file-count limit without hanging.
- [ ] Test DNS, ping timeout and one TCP port check; verify failures are communicated clearly.
- [ ] Confirm no module claims malware detection, safe/unsafe verdict, real-time protection, or quarantine unless actually implemented and independently tested.
- [ ] Test on a device without Internet access; core file and link tools should remain usable.
- [ ] Check unexpected permission/IO errors and startup logging.

## Commercial package
- [ ] Package is reproducible and its SHA-256 checksum recorded.
- [ ] Buyer guide, version notes, and uninstall/data-retention guidance are included.
- [ ] Source-distribution and binary-license terms are reviewed.
- [ ] Screenshots come from the actual release build.
- [ ] Listing accurately describes the implemented MVP and names unavailable features.
- [ ] Price, update policy, support scope, and return/refund terms are defined.
- [ ] Installer/uninstaller and user-data preservation have been manually verified.

Record commit SHA, CI links, tested Windows versions, test date, checksum, and unresolved issues before release.
