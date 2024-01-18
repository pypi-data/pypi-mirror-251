from typing import Any, Iterable, Optional, Callable

import click
from yaml import dump as to_yaml_string, SafeDumper

from dnastack.cli.helpers.base_iterator_printer import BaseIteratorPrinter, I, R
from dnastack.cli.helpers.exporter import normalize
from dnastack.feature_flags import in_interactive_shell, cli_show_list_item_index


class YamlIteratorPrinter(BaseIteratorPrinter):
    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,
              decimal_as: str = 'string',
              sort_keys: bool = True  # NOTE: Declared but ignored
              ) -> int:
        row_count = 0

        for row in iterator:
            if limit and row_count >= limit:
                break

            entry = transform(row) if transform else row
            normalized = normalize(entry)
            encoded = (
                normalized
                if isinstance(normalized, str)
                else to_yaml_string(normalize(entry),
                                    Dumper=SafeDumper,
                                    sort_keys=False)
            )

            click.echo('- ', nl=False)
            click.echo(
                '\n'.join([
                    f'  {line}'
                    for line in encoded.split('\n')
                ]).strip(),
                nl=False
            )

            if in_interactive_shell and item_marker:
                marker = item_marker(row)
                if marker:
                    click.secho(f' # {marker}', fg='green', err=True, nl=False)

            if in_interactive_shell and cli_show_list_item_index:
                click.secho(f' # {row_count}', dim=True, err=True, nl=False)

            click.echo()

            row_count += 1

        if row_count == 0:
            click.echo('[]')

        return row_count
