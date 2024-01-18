import math
import shutil
from typing import Any, Iterable, Optional, Callable, List

import click

from dnastack.cli.helpers.base_iterator_printer import BaseIteratorPrinter, I, R
from dnastack.cli.helpers.exporter import normalize
from dnastack.feature_flags import in_interactive_shell

NON_INTERACTIVE_SHELL_MAX_ROWS = 1000


class TableIteratorPrinter(BaseIteratorPrinter):

    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,  # NOTE: Declared but ignored
              decimal_as: str = 'string',
              sort_keys: bool = True  # NOTE: Declared but ignored
              ) -> int:
        terminal_columns_size, terminal_rows_size = shutil.get_terminal_size((80, 20))
        terminal_rows_size -= 3
        row_count = 0
        buffer = []
        paginate_printer = None
        for row in iterator:
            if limit and row_count >= limit:
                break

            entry = transform(row) if transform else row
            normalized = normalize(entry, map_decimal=str if decimal_as == 'string' else float, sort_keys=sort_keys)
            if row_count == 0:
                paginate_printer = PaginateTablePrinter(normalized.keys(), terminal_columns_size)
            buffer.append(normalized)
            row_count += 1
            if row_count % terminal_rows_size == 0:
                paginate_printer.print(buffer)
                buffer = []
                if in_interactive_shell:
                    self.wait_continue(row_count)
                else:
                    if row_count > NON_INTERACTIVE_SHELL_MAX_ROWS:
                        msg = f'ATTENTION: its not the entire result, first {NON_INTERACTIVE_SHELL_MAX_ROWS} are loaded'
                        click.echo(msg)
                        break

        paginate_printer.print(buffer)
        return row_count

    @staticmethod
    def wait_continue(loaded_row_count: int):
        input(f"\n {loaded_row_count} rows are loaded, press Enter to continue...")
        print("\033[A                                                      \033[A")


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

    def __init__(self, headers: List[str], terminal_columns_size: int):
        self.headers = headers
        self.terminal_columns_size = terminal_columns_size
        self.widths: Optional[dict] = None

    def print(self, buffer: List[Any]):
        if not self.widths:
            self.setup_headers_and_columns(buffer)
        for item in buffer:
            click.echo('')
            [self.stylish_print(header, item[header] if header in item else '') for header in self.headers]

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
        click.echo(click.style(text, fg=fg, bg=bg), nl=False)
        click.echo(click.style('|', fg='blue'), nl=False)

    @staticmethod
    def find_median(length_list: List[int]):
        median = sorted(length_list)[int(math.floor(len(length_list) / 2))]
        return median

    def setup_headers_and_columns(self, buffer: List[Any]):
        self.widths = self.calculate_columns_width(buffer)
        [self.stylish_print(key=header, value=header, is_header=True) for header in self.headers]

    def calculate_columns_width(self, sample_data) -> dict:
        calculated_widths, columns_content_length = {}, {}
        column_values = {header: [] for header in self.headers}
        for row in sample_data:
            for header in self.headers:
                column_values[header].append(str(row[header]) if header in row else '')

        for header in self.headers:
            columns_content_length[header] = int(self.find_median([len(s) for s in column_values[header]]))

        total_width = sum(columns_content_length[header] for header in self.headers)
        remained_terminal_space = self.terminal_columns_size
        for header in self.headers:
            portion = columns_content_length[header] / total_width
            calculated_widths[header] = int(portion * remained_terminal_space)
            # limit column width to double the median, even if we have space available
            maximum_desired_width = int(2 * columns_content_length[header]) - 1
            # exceptionally allow giving more space, if the header is lengthy
            maximum_desired_width = max(maximum_desired_width, len(header))
            calculated_widths[header] = min(calculated_widths[header], maximum_desired_width)
            # deducting allocated space
            total_width -= columns_content_length[header]
            remained_terminal_space -= calculated_widths[header]
        return calculated_widths
