# Berry desktop source

This repository owns the selected reusable configuration and six canonical guides.
Read README.md, NOTICE.md and source-selection.json before changing the selection.

- Keep application-native configuration and personal overrides separate.
- Do not copy artwork, credentials, machine identities or private operational state.
- Changes to selected configuration require reviewed hashes and transformation notes.
- Do not execute presets, replace live configuration, install packages or reload a
  compositor as part of source verification.
- Keep syntax/integrity evidence distinct from application/session acceptance.
- Validate with the read-only verifier and disposable-copy tests documented below.

```sh
python3 -I -S -B tools/verify.py
python3 -I -S -B -m unittest discover -s tests -v
```
