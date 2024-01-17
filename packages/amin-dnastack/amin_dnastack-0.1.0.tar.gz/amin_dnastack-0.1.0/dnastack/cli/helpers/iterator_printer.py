import math
import sys

import shutil
import csv
from json import dumps as to_json_string

import click
from pydantic import BaseModel
from typing import TypeVar, Any, Iterable, Optional, Callable, List
from yaml import dump as to_yaml_string, SafeDumper

from dnastack.cli.helpers.exporter import normalize
from dnastack.feature_flags import in_interactive_shell, cli_show_list_item_index

I = TypeVar('I')
R = TypeVar('R')


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
    elif output_format == OutputFormat.FIXED_WIDTH:
        printer = FixedWidthPrinter()
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
    FIXED_WIDTH = 'fixed_width'

    DEFAULT_FOR_RESOURCE = YAML
    DEFAULT_FOR_DATA = JSON


class BaseIteratorPrinter:
    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,
              decimal_as: str = 'string',
              sort_keys: bool = True):
        raise NotImplementedError()


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


class FixedWidthPrinter(BaseIteratorPrinter):

    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,  # NOTE: Declared but ignored
              decimal_as: str = 'string',
              sort_keys: bool = True  # NOTE: Declared but ignored
              ) -> int:
        terminal_columns_size, terminal_rows_size = shutil.get_terminal_size((80, 20))
        row_count = 0
        buffer = []
        pprinter = None
        for row in iterator:
            if limit and row_count >= limit:
                break

            entry = transform(row) if transform else row
            normalized = normalize(entry, map_decimal=str if decimal_as == 'string' else float, sort_keys=sort_keys)
            if row_count == 0:
                pprinter = FixedWidthHandler(normalized.keys(), terminal_columns_size)
            buffer.append(normalized)
            row_count += 1
            if row_count % terminal_rows_size == 0:
                pprinter.print(buffer)
                buffer = []
                if in_interactive_shell:
                    input(f"\n {row_count} rows are loaded, press Enter to continue...")
                    print("\033[A                                                      \033[A")
        pprinter.print(buffer)
        return row_count


class FixedWidthHandler:
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
        self.widths = None

    def print(self, buffer: List[Any]):
        if not self.widths:
            self.setup_headers_and_columns(buffer)
        for item in buffer:
            click.echo('')
            [self.stylish_print(header, item[header] if header in item else '') for header in self.headers]

    def stylish_print(self, key: str, value: Any, is_header: bool = False):
        width = int(self.widths[key]) - 1
        text = f'{(str(value or ""))[0:width] : ^{width}}'
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
        self.widths = self.calculate_column_widths(buffer)
        [self.stylish_print(key=header, value=header, is_header=True) for header in self.headers]

    def calculate_column_widths(self, sample_data):
        column_widths = {}
        values = {h: [] for h in self.headers}
        medians = {}
        for row in sample_data:
            for h in self.headers:
                values[h].append(str(row[h]) if h in row else '')

        for h in self.headers:
            medians[h] = int(self.find_median([len(s) for s in values[h]]))

        _sum = sum(medians[h] for h in self.headers)
        remained_space = self.terminal_columns_size
        for h in self.headers:
            portion = medians[h] / _sum
            column_widths[h] = int(portion * remained_space)
            column_widths[h] = min(column_widths[h], max(int(2 * medians[h]) - 1, len(h)))
            _sum -= medians[h]
            remained_space -= column_widths[h]
        return column_widths


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
