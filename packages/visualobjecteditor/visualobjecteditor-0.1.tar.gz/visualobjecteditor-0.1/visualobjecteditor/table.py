import re
from abc import ABC
from dataclasses import dataclass, replace
from functools import cached_property
from re import Pattern
from typing import Callable, Iterable, Iterator, Optional

import tabulate

from visualobjecteditor.base import (
    Document,
    InvalidSerializationError,
    ParseError,
    SerializationResult,
    T,
    VisualObjectEditor,
)
from visualobjecteditor.utils import join_with_empty_line, split_on_empty_lines

tabulate.PRESERVE_WHITESPACE = True


def _default_strip_cells(cell: str, _column_id: int) -> str:
    return cell.strip()


@dataclass(frozen=True)
class TableFormatter:
    column_divider: str = '|'
    headers: Optional[list[str]] = None
    header_separator: Optional[str] = '-'
    padding: int = 1
    strip_cells: bool = True
    cell_stripper: Callable[[str, int], str] = _default_strip_cells
    max_columns: Optional[int] = None
    ignore_divider_in_last_column: bool = False
    ignore_empty_lines: bool = True

    @property
    def header_row_count(self):
        if self.headers is None:
            return 0
        elif self.header_separator is None:
            return 1
        else:
            return 2

    def get_formatter_for_prepended_id_column(self) -> 'TableFormatter':
        return replace(
            self,
            headers=None if self.headers is None else ["ID", *self.headers],
            strip_cells=True,
            cell_stripper=lambda cell, n: cell.strip() if n == 0 else (
                self.cell_stripper(cell, n - 1) if self.strip_cells else cell
            ),
            max_columns=None if self.max_columns is None else self.max_columns + 1,
        )

    def _strip_cell(self, cell: str, column_id: int) -> str:
        if self.strip_cells:
            return self.cell_stripper(cell, column_id)
        else:
            return cell

    @cached_property
    def _column_divider(self) -> str:
        return f"{' ' * self.padding}{self.column_divider}{' ' * self.padding}"

    @cached_property
    def _column_divider_pattern(self) -> Pattern:
        return re.compile(fr'\s{{0,{self.padding}}}{re.escape(self.column_divider)}\s{{0,{self.padding}}}')

    def serialize_table(self, tabular_data: Iterable[list[str]]) -> list[str]:
        tabular_data = list(tabular_data)

        for row in tabular_data:
            for column_id, cell in enumerate(row):
                if self.max_columns is not None and column_id >= self.max_columns:
                    raise InvalidSerializationError(f"Serialized data contains more than {self.max_columns} columns.")
                if '\n' in cell:
                    raise InvalidSerializationError("Serialized cell contains a line break.")
                if self.column_divider in cell and (
                        self.max_columns is None
                        or column_id < self.max_columns - 1
                        or not self.ignore_divider_in_last_column
                ):
                    raise InvalidSerializationError(
                        f"Serialized cell contains a column divider character ('{self.column_divider}').",
                    )

                row[column_id] = self._strip_cell(cell, column_id)

        return tabulate.tabulate(
            tabular_data=tabular_data,
            headers=() if self.headers is None else self.headers,
            tablefmt=tabulate.TableFormat(
                lineabove=None,
                linebelowheader=(
                    None
                    if self.header_separator is None
                    else tabulate.Line("", self.header_separator, self._column_divider, "")
                ),
                linebetweenrows=None,
                linebelow=None,
                headerrow=tabulate.DataRow("", self._column_divider, ""),
                datarow=tabulate.DataRow("", self._column_divider, ""),
                padding=0,
                with_header_hide=None,
            ),
        ).splitlines()

    def serialize_table_with_ids(self, tabular_data: Iterable[tuple[str, list[str]]]) -> list[str]:
        return self.get_formatter_for_prepended_id_column().serialize_table(
            ([column_id, *row] for column_id, row in tabular_data),
        )

    def parse_row(self, serialized_table_row: str) -> list[str]:
        row = [
            self._strip_cell(cell, column_id)
            for column_id, cell in enumerate(self._column_divider_pattern.split(
                serialized_table_row,
                maxsplit=(
                    self.max_columns - 1
                    if self.max_columns is not None and self.ignore_divider_in_last_column
                    else 0
                ),
            ))
        ]

        if self.max_columns is not None and not self.ignore_divider_in_last_column and len(row) > self.max_columns:
            raise ParseError(f"Row contains more than {self.max_columns} columns.")

        return row

    def parse_rows(self, serialized_table_rows: list[str]) -> Iterator[list[str]]:
        for row in serialized_table_rows[self.header_row_count:]:
            parsed_row = self.parse_row(row)
            if not self.ignore_empty_lines or len(parsed_row) != 1 or parsed_row[0] != "":
                yield parsed_row

    def parse_rows_with_id(self, serialized_table_rows: list[str]) -> Iterator[tuple[Optional[str], list[str]]]:
        for row in self.get_formatter_for_prepended_id_column().parse_rows(serialized_table_rows):
            yield row[0], row[1:]


DEFAULT_TABLE_FORMATTER = TableFormatter()


@dataclass(kw_only=True)
class TableRowObjectEditor(VisualObjectEditor[list[str], T]):
    table_formatter: TableFormatter = DEFAULT_TABLE_FORMATTER

    def build_documents(self, rows: Iterable[SerializationResult[list[str]]]) -> Iterator[Document]:
        if self.tracking_mode:
            yield Document(lines=self.table_formatter.serialize_table_with_ids(
                (row.object_id, row.data) for row in rows
            ))
        else:
            yield Document(lines=self.table_formatter.serialize_table(row.data for row in rows))

    def split_documents(self, documents: Iterable[Document]) -> Iterator[tuple[Optional[str], list[str]]]:
        for document in documents:
            if self.tracking_mode:
                yield from self.table_formatter.parse_rows_with_id(document.lines)
            else:
                for row in self.table_formatter.parse_rows(document.lines):
                    yield None, row


@dataclass(kw_only=True)
class TableObjectEditor(VisualObjectEditor[list[list[str]], T], ABC):
    table_formatter: TableFormatter = DEFAULT_TABLE_FORMATTER
    create_individual_documents: bool = False
    id_cell_row: int = 0
    id_cell_column: int = 0

    def build_documents(self, tables: Iterable[SerializationResult[list[list[str]]]]) -> Iterator[Document]:
        serialized_tables = []

        for table in tables:
            if self.tracking_mode:
                table_data = [row.copy() for row in table.data]

                if table_data[self.id_cell_row][self.id_cell_column] is not None:
                    raise InvalidSerializationError("Serialized table contains data in its ID cell.")

                table_data[self.id_cell_row][self.id_cell_column] = table.object_id
            else:
                table_data = table.data

            serialized_tables.append(self.table_formatter.serialize_table(table_data))

        if self.create_individual_documents:
            for table_lines in serialized_tables:
                yield Document(lines=table_lines)
        else:
            yield Document(lines=list(join_with_empty_line(serialized_tables)))

    def split_documents(self, documents: Iterable[Document]) -> Iterator[tuple[Optional[str], list[list[str]]]]:
        for document in documents:
            for block_lines in split_on_empty_lines(document.lines):
                table = list(self.table_formatter.parse_rows(block_lines))

                object_id = None

                if self.tracking_mode:
                    object_id = table[self.id_cell_row][self.id_cell_column]
                    table[self.id_cell_row][self.id_cell_column] = None

                yield object_id, table
