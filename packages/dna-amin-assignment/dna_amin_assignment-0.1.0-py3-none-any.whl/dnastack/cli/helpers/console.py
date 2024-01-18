import shutil
from abc import ABC

import click

from dnastack.feature_flags import in_interactive_shell


class BaseConsole(ABC):

    def is_interactive(self) -> bool:
        raise NotImplementedError()

    def print_new_line(self):
        raise NotImplementedError()

    def print_text(self, text):
        raise NotImplementedError()

    def print_pretty_text(self, text: str, bg: str, fg: str):
        raise NotImplementedError()

    def wait_for_enter(self, msg: str):
        raise NotImplementedError()

    def get_columns_size(self):
        raise NotImplementedError()

    def get_rows_size(self):
        raise NotImplementedError()


class Console(BaseConsole):
    def __init__(self):
        self.columns_size, self.rows_size = shutil.get_terminal_size((80, 20))

    def is_interactive(self) -> bool:
        return in_interactive_shell

    def print_new_line(self):
        click.echo('')

    def print_text(self, text):
        click.echo(text, nl=False)

    def print_pretty_text(self, text: str, bg: str, fg: str):
        click.echo(click.style(text, fg=fg, bg=bg), nl=False)

    def wait_for_enter(self, msg: str):
        input(msg)
        self._remove_temp_text()

    def get_columns_size(self):
        return self.columns_size

    def get_rows_size(self):
        return self.rows_size - 3

    @staticmethod
    def _remove_temp_text():
        print("\033[A\033[A\033[A")
