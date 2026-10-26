-- Berry minimal Hyprland Lua preset; API compatibility must be checked locally.
-- Super+Enter: Foot; Super+D: Fuzzel. No lock, idle or session manager supplied.
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })
hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")
hl.config({
    general = {
        gaps_in = 3, gaps_out = 6, border_size = 1,
        col = { active_border = { colors = { "rgba(8e977bff)" }, angle = 0 }, inactive_border = "rgba(363d3bff)" },
        resize_on_border = true, allow_tearing = false, layout = "dwindle",
    },
    decoration = {
        rounding = 3, active_opacity = 1.0, inactive_opacity = 1.0,
        blur = { enabled = false }, shadow = { enabled = false },
    },
    animations = { enabled = true },
    -- Use damage scheduling instead of continuously repainting an unchanged desktop.
    debug = { vfr = true },
    dwindle = { preserve_split = true },
    input = {
        kb_layout = "us", follow_mouse = 1,
        touchpad = { natural_scroll = true, tap_to_click = true, disable_while_typing = true },
    },
    misc = { disable_hyprland_logo = true, force_default_wallpaper = 0 },
})
local function app(keys, command) hl.bind(keys, hl.dsp.exec_cmd(command)) end
app("SUPER + Return", "foot")
app("SUPER + D", "fuzzel")
app("SUPER + E", "pcmanfm")
app("SUPER + B", "librewolf")
app("SUPER + C", "zeditor")
hl.bind("SUPER + Q", hl.dsp.window.close())
hl.bind("SUPER + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind("SUPER + F", hl.dsp.window.fullscreen({ action = "toggle" }))
for _, dir in ipairs({ "left", "right", "up", "down" }) do
    hl.bind("SUPER + " .. dir, hl.dsp.focus({ direction = dir }))
    hl.bind("SUPER + SHIFT + " .. dir, hl.dsp.window.move({ direction = dir }))
end
for workspace = 1, 9 do
    hl.bind("SUPER + " .. workspace, hl.dsp.focus({ workspace = workspace }))
    hl.bind("SUPER + SHIFT + " .. workspace, hl.dsp.window.move({ workspace = workspace }))
end
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
local repeatKeys = { locked = true, repeating = true }
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), repeatKeys)
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), repeatKeys)
hl.bind("XF86AudioMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), { locked = true })
hl.bind("XF86AudioMicMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"), { locked = true })
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"), repeatKeys)
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"), repeatKeys)
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), { locked = true })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"), { locked = true })
