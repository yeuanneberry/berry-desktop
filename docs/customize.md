# Customize without a second baseline

## Keep reusable and personal choices separate

Clone or fork when you want to follow upstream changes. A template copy is a new
starting snapshot and will not receive fixes automatically. A personal branch can
hold experiments, but it is not private storage. Keep your own overlay outside
the public repository and never commit credentials or identifiers.

Native application composition is preferable to a long-lived full configuration
fork. Merge only the sections you need when an application's native configuration
has no suitable include mechanism. Do not assume every app understands an `include`.

## Kitty includes

In your own `kitty.conf`, use an include for a reviewed baseline copy and put
personal settings afterward. Kitty resolves relative includes from its config:

```text
include berry.conf
font_size 12.0
background_opacity 1.0
```

Here `berry.conf` is your staged copy of this repository's Kitty preset beside
your own file. The later values express your preferences. A portable baseline
does not require Fish or overwrite your chosen login shell.

## Themes and app preferences

Select the Qt6ct palette through Qt6ct after copying only the color-scheme file;
keep your existing Qt6ct configuration. Install the Btop theme separately and
select `berry` in Btop. GPU box/device selection remains local; the portable
preset uses CPU, memory, network and process panels.

GTK's supplied `Berry` theme is GTK 3 only. It imports installed Adwaita resources.
Selecting it is a separate application/desktop preference; this candidate does
not change GTK environment variables or force a theme on all applications.

For Foot, Fuzzel, Mako, mpv and Zathura, merge the reviewed settings into your
existing native config or stage a complete replacement. Keep terminal choice,
font availability, output backend and accessibility preferences explicit.

## Hardware and identity

No monitor name, display scale, device ID, username, home mount or machine-specific
service belongs in this baseline. Keep those local. Full session orchestration,
power helpers, package management and account-dependent automation are deliberately
outside this initial collection.
