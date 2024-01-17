import sys
import termios
import tty
from typing import Callable, Iterable, Iterator, TypeVar

from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

T = TypeVar("T")  # object type


def group_until(
        objects: Iterable[T],
        new_group_condition: Callable[[T], bool],
        *,
        add_to_previous_group: bool = True,
        add_to_next_group: bool = False,
        yield_empty_groups: bool = False,
) -> Iterator[list[T]]:
    current_group = []

    for obj in objects:
        is_group_end = new_group_condition(obj)

        if add_to_previous_group or not is_group_end:
            current_group.append(obj)

        if is_group_end and (yield_empty_groups or current_group):
            yield current_group
            current_group = []

        if add_to_next_group and is_group_end:
            current_group.append(obj)

    if yield_empty_groups or current_group:
        yield current_group


def split_on_empty_lines(lines: Iterable[str]) -> Iterator[list[str]]:
    return group_until(
        lines,
        new_group_condition=lambda line: not line.strip(),
        add_to_previous_group=False,
    )


def join_with_empty_line(line_groups: Iterable[Iterable[str]], *, empty_line_count: int = 1) -> Iterator[str]:
    for n, lines in enumerate(line_groups):
        if n != 0:
            for _ in range(empty_line_count):
                yield ""
        yield from lines


def read_key() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_fullscreen_choice(message: str, title: str, border_style: str, choices: dict[str, str]) -> str:
    message_lines = [
        message,
        "",
        "Choose an option to continue:",
        "",
    ]

    for option_key, option_title in choices.items():
        message_lines.append(f"   [bold cyan][{option_key}][/bold cyan] {option_title}")

    layout = Layout(
        Align.center(
            Panel(
                "\n".join(message_lines),
                box=box.ROUNDED,
                padding=(1, 4),
                title=f"[b {border_style}]{title}",
                border_style=border_style,
                expand=False,
            ),
            vertical="middle",
        ),
        name="root",
    )

    with Live(layout, auto_refresh=False, transient=True):
        key = None
        while key not in choices:
            key = read_key().upper()

    return key
