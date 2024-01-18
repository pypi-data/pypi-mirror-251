import math
from typing import Any, Iterable, Optional, Callable, List

from dnastack.cli.helpers.base_iterator_printer import BaseIteratorPrinter, I, R
from dnastack.cli.helpers.console import Console, BaseConsole
from dnastack.cli.helpers.exporter import normalize

NON_INTERACTIVE_SHELL_MAX_ROWS = 1000


class TableIteratorPrinter(BaseIteratorPrinter):
    def __init__(self):
        self.console = Console()

    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,  # NOTE: Declared but ignored
              decimal_as: str = 'string',
              sort_keys: bool = True  # NOTE: Declared but ignored
              ) -> int:
        row_count = 0
        paginate_printer = None
        for row in iterator:
            if limit and row_count >= limit:
                break

            entry = transform(row) if transform else row
            normalized = normalize(entry, map_decimal=str if decimal_as == 'string' else float, sort_keys=sort_keys)
            if row_count == 0:
                paginate_printer = PaginateTablePrinter(normalized.keys(), self.console)

            paginate_printer.print(normalized, row_count)
            row_count += 1
            if row_count > NON_INTERACTIVE_SHELL_MAX_ROWS:
                paginate_printer.flush_buffer()
                msg = f'\n ATTENTION: its not the entire result, first {NON_INTERACTIVE_SHELL_MAX_ROWS} are loaded'
                self.console.print_text(msg)
                break
        paginate_printer.flush_buffer()
        return row_count


class PaginateTablePrinter:
    default_formats = {
        'state': {
            'fg': 'red',
        },
        'date': {
            'bg': 'blue'
        },
        'country': {
            'bg': 'green'
        }
    }

    def __init__(self, headers: List[str], console: BaseConsole):
        self.buffer = []
        self.headers = headers
        self.widths: Optional[dict] = None
        self.console = console

    @property
    def width(self):
        if self.widths:
            return sum(self.widths.values())
        return -1

    def print(self, row, row_count: int):
        if self.widths:
            self.print_row(row)
            if self.console.is_interactive() and (row_count % self.console.get_rows_size() == 0):
                self.wait_continue(row_count)
        else:
            self.buffer.append(row)
            if len(self.buffer) >= self.console.get_rows_size() :
                self.flush_buffer()
                self.buffer = []

    def flush_buffer(self):
        if not self.widths:
            self.setup_headers_and_columns(self.buffer)
            for row in self.buffer:
                self.print_row(row)

    def print_row(self, row):
        self.console.print_new_line()
        [self.stylish_print(header, row[header] if header in row else '') for header in self.headers]

    def wait_continue(self, loaded_row_count: int):
        self.console.wait_for_enter(f"\n {loaded_row_count} rows loaded, press Enter to continue... (cancel by ctrl+c)")

    def stylish_print(self, key: str, value: Any, is_header: bool = False):
        width = int(self.widths[key]) - 1
        # cut and center the text, strip to remove spaces or new lines
        text = f'{(str(value or "").strip())[0:width] : ^{width}}'
        fg = None
        bg = None
        formats = self.default_formats
        if key in formats:
            if 'fg' in formats[key]:
                fg = formats[key]['fg']
            if 'bg' in formats[key]:
                bg = formats[key]['bg']
        if is_header:
            fg, bg = 'black', 'red'
        self.console.print_pretty_text(text, bg, fg)
        self.console.print_pretty_text('|', bg=None, fg='blue')

    @staticmethod
    def find_median(length_list: List[int]):
        median = sorted(length_list)[int(math.floor(len(length_list) / 2))]
        return max(median, 2)

    def setup_headers_and_columns(self, buffer: List[Any]):
        self.widths = self.calculate_columns_width(buffer)
        [self.stylish_print(key=header, value=header, is_header=True) for header in self.headers]

    def calculate_columns_width(self, sample_data: List) -> dict:
        calculated_widths, columns_content_length = {}, {}
        column_values = {header: [] for header in self.headers}
        for row in sample_data:
            for header in self.headers:
                column_values[header].append(str(row[header]) if header in row else '')

        for header in self.headers:
            columns_content_length[header] = int(self.find_median([len(s) for s in column_values[header]]))

        total_width = sum(columns_content_length[header] for header in self.headers)
        remained_terminal_space = self.console.get_columns_size()
        for header in self.headers:
            portion = columns_content_length[header] / total_width
            calculated_widths[header] = int(portion * remained_terminal_space)
            # limit column width to double the median, even if we have space available
            maximum_desired_width = int(2 * columns_content_length[header]) - 1
            # if the header is lengthy & we have space, give the space
            maximum_desired_width = max(maximum_desired_width, len(header))
            calculated_widths[header] = min(calculated_widths[header], maximum_desired_width)
            # deducting allocated space
            total_width -= columns_content_length[header]
            remained_terminal_space -= calculated_widths[header]
        return calculated_widths
