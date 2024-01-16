# [ender-ansi](https://github.com/endercat126/ender-ansi)
🌈 uwu cutesy rainbow text <3 ✨

this package is just a quicker way to colour your text

## usage

```python
from ender_ansi import *

print(f"{fg.pink}Hello, World!{fx.reset}")
print(f"{fg.cyan}This is {fg.green}{fx.bold}very {fx.italic}cool!{fx.reset}")
```

## install
```bash
pip install ender_ansi
```

## colours

- black 🖤
- red ❤️
- green 💚
- yellow 💛
- blue 💙
- pink/magenta 💜
- cyan/aqua 🩵
- white 🤍

## effects

- reset
- bold/strong
- dull/dim/faint
- italic/oblique
- underline
- reverse/invert/inverse
- strikethrough/disabled/linethrough/crossedout

## functions
> clear()
    Clears the terminal screen

> clear_all()
    Clears the terminal, including the scrollback buffer, and resets the cursor position

> clear_line()
    Clears the current line at the cursor

> move_cursor(row, col)
    Moves the cursor to a given row and column


## license
This project is released into the public domain under The Unlicense.
See LICENSE for more information.

