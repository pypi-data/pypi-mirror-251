from typing import Any, Iterable, Optional, Callable

from dnastack.cli.helpers.base_iterator_printer import I, R
from dnastack.cli.helpers.printers.csv_iterator_printer import CsvIteratorPrinter
from dnastack.cli.helpers.printers.json_iterator_printer import JsonIteratorPrinter
from dnastack.cli.helpers.printers.table_iterator_printer import TableIteratorPrinter
from dnastack.cli.helpers.printers.yaml_iterator_printer import YamlIteratorPrinter


def show_iterator(output_format: str,
                  iterator: Iterable[Any],
                  transform: Optional[Callable[[I], R]] = None,
                  limit: Optional[int] = None,
                  item_marker: Optional[Callable[[Any], Optional[str]]] = None,
                  decimal_as: str = 'string',
                  sort_keys: bool = True) -> int:
    """ Display the result from the iterator """
    if output_format == OutputFormat.JSON:
        printer = JsonIteratorPrinter()
    elif output_format == OutputFormat.YAML:
        printer = YamlIteratorPrinter()
    elif output_format == OutputFormat.CSV:
        printer = CsvIteratorPrinter()
    elif output_format == OutputFormat.TABLE:
        printer = TableIteratorPrinter()
    else:
        raise ValueError(f'The given output format ({output_format}) is not available.')

    return printer.print(iterator,
                         transform=transform,
                         limit=limit,
                         item_marker=item_marker,
                         decimal_as=decimal_as,
                         sort_keys=sort_keys)


class OutputFormat:
    JSON = 'json'
    YAML = 'yaml'
    CSV = 'csv'
    TABLE = 'table'

    DEFAULT_FOR_RESOURCE = YAML
    DEFAULT_FOR_DATA = JSON



