from json import dumps as to_json_string
from typing import Any, Iterable, Optional, Callable

import click

from dnastack.cli.helpers.base_iterator_printer import BaseIteratorPrinter, I, R
from dnastack.cli.helpers.exporter import normalize
from dnastack.feature_flags import in_interactive_shell, cli_show_list_item_index


class JsonIteratorPrinter(BaseIteratorPrinter):
    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,  # NOTE: Declared but ignored
              decimal_as: str = 'string',
              sort_keys: bool = True) -> int:
        row_count = 0

        for row in iterator:
            if limit and row_count >= limit:
                break

            if row_count == 0:
                # First row
                click.echo('[')
            else:
                click.echo(',', nl=False)

                if in_interactive_shell and cli_show_list_item_index:
                    click.secho(f' # {row_count}', dim=True, err=True, nl=False)

                click.echo('')  # just a new line

            entry = transform(row) if transform else row
            normalized = normalize(entry, map_decimal=str if decimal_as == 'string' else float, sort_keys=sort_keys)
            encoded = to_json_string(normalized, indent=2, sort_keys=False)

            click.echo(
                '\n'.join([
                    f'  {line}'
                    for line in encoded.split('\n')
                ]),
                nl=False
            )

            row_count += 1

        if row_count == 0:
            click.echo('[]')
        else:
            click.echo('\n]')

        return row_count
