from datetime import datetime
from pathlib import Path
import stat

from core import apply_style


class Column:
    def __init__(self) -> None:
        self.items: list[str] = []
        self.max_length = 0

    def append(self, item: str) -> None:
        self.items.append(item)
        self.max_length = max(self.max_length, len(item))


def iter_path(path: Path) -> list[tuple[str, Path]]:
    path = path.resolve()
    if not path.is_dir():
        return [(path.name, path)]

    special_entries = [(".", path), ("..", path.parent)]
    items = ((p.name, p) for p in path.iterdir())
    return special_entries + sorted(
        items, key=lambda it: (not it[1].is_dir(), it[0].casefold())
    )


def format_directory_listing(
    path: Path, dir_style: str = ""
) -> tuple[str, int]:
    """Returns a formatted, ls -la style string for the given directory and the number of lines in the string."""
    perms = Column()
    sizes = Column()
    timestamps = Column()
    entries: list[str] = []

    for name, it in iter_path(path):
        it_stat = it.lstat()
        is_dir = it.is_dir()

        perms.append(stat.filemode(it_stat.st_mode))

        sizes.append(str(it_stat.st_size))
        timestamps.append(
            datetime.fromtimestamp(it_stat.st_mtime).strftime("%b %d %H:%M")
        )

        if is_dir:
            name = apply_style(name, dir_style)

        entries.append(name)

    rows = 0
    pad = " " * 2
    result = ""
    for perm, size, timestamp, entry in zip(
        perms.items, sizes.items, timestamps.items, entries
    ):
        row = perm.rjust(perms.max_length) + pad
        row += size.rjust(sizes.max_length) + pad
        row += timestamp.rjust(timestamps.max_length) + pad
        row += entry

        result += row + "\n"
        rows += 1

    return result, rows
