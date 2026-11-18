import sys

ESC = "\033["  # ] STUPID NVIM
RESET = f"{ESC}0m"
ENABLE_ALT_BUFFER = f"{ESC}?1049h"
DISABLE_ALT_BUFFER = f"{ESC}?1049l"
CLEAR_SCREEN = f"{ESC}2J"
GOTO_HOME = f"{ESC}H"


def rgb(r: int, g: int, b: int, bg: bool = False) -> str:
    code = 48 if bg else 38
    return f"{ESC}{code};2;{r};{g};{b}m"


def apply_style(s: str, style: str) -> str:
    return style + s + RESET


def enter_alt_buffer() -> None:
    sys.stdout.write(ENABLE_ALT_BUFFER + CLEAR_SCREEN + GOTO_HOME)
    sys.stdout.flush()


def exit_alt_buffer() -> None:
    sys.stdout.write(DISABLE_ALT_BUFFER)
    sys.stdout.flush()
