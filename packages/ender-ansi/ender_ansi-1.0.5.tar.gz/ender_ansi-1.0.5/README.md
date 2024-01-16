# [ender-ansi](https://pypi.org/project/ender-ansi/)
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
- ![🖤 black](https://img.shields.io/static/v1?label=&message=black&color=313244&style=for-the-badge)
- ![❤️ red](https://img.shields.io/static/v1?label=&message=red&color=f38ba8&style=for-the-badge)
- ![💚 green](https://img.shields.io/static/v1?label=&message=green&color=a6e3a1&style=for-the-badge)
- ![💛 yellow](https://img.shields.io/static/v1?label=&message=yellow&color=f9e2af&style=for-the-badge)
- ![💙 blue](https://img.shields.io/static/v1?label=&message=blue&color=89b4fa&style=for-the-badge)
- ![💜 pink/magenta](https://img.shields.io/static/v1?label=&message=pink/magenta&color=f5c2e7&style=for-the-badge)
- ![🩵 cyan/aqua](https://img.shields.io/static/v1?label=&message=cyan/aqua&color=94e2d5&style=for-the-badge)
- ![🤍 white](https://img.shields.io/static/v1?label=&message=white&color=cdd6f4&style=for-the-badge)

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

