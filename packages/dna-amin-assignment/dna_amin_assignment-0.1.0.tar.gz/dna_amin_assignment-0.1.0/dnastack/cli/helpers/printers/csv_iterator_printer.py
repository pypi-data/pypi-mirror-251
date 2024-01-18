import csv
import sys
from typing import Any, Iterable, Optional, Callable

from dnastack.cli.helpers.base_iterator_printer import BaseIteratorPrinter, I, R
from dnastack.cli.helpers.exporter import normalize


class CsvIteratorPrinter(BaseIteratorPrinter):
    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,  # NOTE: Declared but ignored
              decimal_as: str = 'string',
              sort_keys: bool = True  # NOTE: Declared but ignored
              ) -> int:
        row_count = 0

        writer = csv.writer(sys.stdout)
        headers = []

        for row in iterator:
            if limit and row_count >= limit:
                break

            entry = transform(row) if transform else row
            normalized = normalize(entry, map_decimal=str if decimal_as == 'string' else float, sort_keys=sort_keys)

            if row_count == 0:
                headers.extend(normalized.keys())
                writer.writerow(headers)

            writer.writerow([normalized[h] if h in normalized else None for h in headers])

            row_count += 1

        return row_count
