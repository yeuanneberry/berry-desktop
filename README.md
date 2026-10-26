# Berry desktop

A small, reusable collection of charcoal, paper, olive and ochre application
configurations from Berry, an Arch Linux desktop, with a minimal native Hyprland
Lua preset and Waybar panel. Keep the parts you like and
compose them with your own settings. There is no wallpaper, bundled font, account
setup, full desktop installer or required personal branch.

Original configuration, tools and guides are available under [MIT](LICENSE).
See [notices](NOTICE.md) for dependencies and scope. Fresh-machine acceptance
has not been established.

- [Overview](docs/overview.md): scope and tested/untested matrix
- [Start](docs/start.md): prerequisites and safe staging
- [Customize](docs/customize.md): native composition and private preferences
- [Apply and recover](docs/apply-recover.md): manual per-app changes and rollback
- [Update](docs/update.md): pinned source, review and drift
- [Reference](docs/reference.md): files, dependencies and troubleshooting

Run the read-only bounded check from this directory:

```sh
python3 -I -S -B tools/verify.py
```

The disposable-copy regression tests run with:

```sh
python3 -I -S -B -m unittest discover -s tests -v
```

This checks reviewed file hashes, path boundaries and local guide links. It does
not launch applications, install packages, change your home, or validate a live
desktop. This public edition owns future reusable changes to the selected files. Private operational history and active deployments stay separate;
they are not repointed by this candidate.
