Notes on keybindings. Serves a few purposes:

- A cheat sheet for useful commands
- Instructions on normalising keybindings across different editors
- Premade configuration files for keymaps


## General settings for each editor

### JetBrains

This includes IntelliJ, PyCharm, RubyMine, etc.

Bindings can be changed at Preferences -> KeyMap.

See also key bindings sub-directories.

Setup and configuration for Jetbrains products, such as PyCharm, IntelliJ IDEA, and GoLand.

Where to find keymaps, as follows. Note that the `keymaps` dir may not exist until a custom keymap
has been created.

- GoLand:
  -  `~/Library/Preferences/GoLand2019.3/keymaps`
  -  `~/Library/Application Support/JetBrains/GoLand2020.1/keymaps`
- PyCharm:
  -  `~/Library/Preferences/PyCharmCE2019.2/keymaps`
  -  `~/Library/Application Support/JetBrains/PyCharmCE2020.1/keymaps`

Find IDE settings with `bash find-ides.sh`.

Instructions on importing a keymap for the first time:

- In IDE, create a new keymap (any keymap) and name it as per the keymap to be imported (e.g.,
  `MattJW-GoLand`). This is a temporary, dummy keymap.
- Close IDE.
- Find the dummy keymap in the `keymaps` dir. Replace it with the keymap being imported.

Other JetBrains dirs...

- `~/Library/Application Support/PyCharmXX`: catalogue with plugins
- `~/Library/Application Support/JetBrains/GoLand2020.1`
- `~/Library/Preferences/PyCharmXX`: the rest of the configuration settings

### VS Code

To do.

## Bindings table

The column for each editor provides instruction on how to configure the given editor for
the given keybinding.

| Action | Key Binding | VS Code | IntelliJ |  |
|--------------------------|------------------|----------|---------|---|
| Cursor to top/bottombottom of file | cmd + down-arrow (or up-arrow) | default  | Move caret to text start |  |
| Multi-cursor: Add cursor by selection | cmd + d | default  | Add selection for next occurrence |  |
| Multi-cursor: Add cursor by mouse click | alt + click | default  |  |  |
| Shift line up/down | alt + down-arrow (or up-arrow) | default  | "Move Line Up" and "Move Line Down" |  |
| Duplicate line up/down | alt + shift + down-arrow (or up-arrow) | default  | "Duplicate Line or Selection" |  |
| Reformat code | alt cmd l |   | default |  |
| Move caret to counterpart brace | ctrl m | ? | default |
