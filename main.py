from pathlib import Path
from typing import Self

import os, sys, shutil, subprocess

ESC = "\033["  # ] STUPID NVIM
RESET = f"{ESC}0m"
ENTER_ALT_BUFFER = f"{ESC}?1049h"
EXIT_ALT_BUFFER = f"{ESC}?1049l"
CLEAR_SCREEN = f"{ESC}2J"
GOTO_HOME = f"{ESC}H"


class Screen:
    def __init__(self) -> None:
        self.buffer = ""
        self.size = shutil.get_terminal_size()

    def __enter__(self) -> None:
        sys.stdout.write(ENTER_ALT_BUFFER + CLEAR_SCREEN + GOTO_HOME)
        sys.stdout.flush()

    def __exit__(self, *_) -> None:  # I don't care
        sys.stdout.write(EXIT_ALT_BUFFER)
        sys.stdout.flush()

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

        self.line(style + s + RESET)

        return self


def rgb(r: int, g: int, b: int, bg: bool = False) -> str:
    code = 48 if bg else 38
    return f"{ESC}{code};2;{r};{g};{b}m"


# TODO: create ls like output without calling the external command ls
def run_ls() -> str:
    res = subprocess.run(["ls", "-la"], stdout=subprocess.PIPE, text=True)
    if res.returncode == 0:
        return res.stdout

    return ""


# NOTE: not memory efficient
def get_lines_in_text(s: str) -> int:
    """This function is not memory efficient! It splites the text into lines, creating a list of strings - just to get its length"""
    return len(s.splitlines())


# TODO: handle overflow of the screen
def main() -> None:
    SURFACE_0 = rgb(49, 50, 68, bg=True)

    cwd = Path.cwd()
    screen = Screen()
    screen.styled_line(cwd.as_posix(), SURFACE_0, filled=True)

    view = run_ls()
    view_lines = get_lines_in_text(view)
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
