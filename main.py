from pathlib import Path
from typing import Self

import os, sys, shutil

from core import apply_style, enter_alt_buffer, exit_alt_buffer, rgb
from file_listing import format_directory_listing


class Screen:
    def __init__(self) -> None:
        self.buffer = ""
        self.size = shutil.get_terminal_size()

    def __enter__(self) -> None:
        enter_alt_buffer()

    def __exit__(self, *_) -> None:  # I don't care
        exit_alt_buffer()

    def text(self, s: str) -> Self:
        self.buffer += s
        return self

    def line(self, s: str) -> Self:
        self.buffer += s + "\n"
        return self

    def filled_line(self, s: str) -> Self:
        self.line(s.ljust(self.size.columns))
        return self

    def present(self) -> None:
        sys.stdout.write(self.buffer)
        sys.stdout.flush()

    def styled_line(self, s: str, style: str, filled: bool = False) -> Self:
        if filled:
            s = s.ljust(self.size.columns)

        self.line(apply_style(s, style))

        return self


# TODO: handle overflow of the screen
def main() -> None:
    SURFACE_0 = rgb(49, 50, 68, bg=True)
    BLUE = rgb(137, 180, 250)

    cwd = Path.cwd()
    screen = Screen()
    screen.styled_line(cwd.as_posix(), SURFACE_0, filled=True)

    view, view_lines = format_directory_listing(cwd, BLUE)
    screen.text(view)

    for _ in range(screen.size.lines - view_lines - 2):  # 2: Header and prompt
        screen.filled_line("")

    with screen:
        screen.present()
        input("$ ")


if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("")  # Enables ANSI colors in legacy Windows cmd.exe

    main()
