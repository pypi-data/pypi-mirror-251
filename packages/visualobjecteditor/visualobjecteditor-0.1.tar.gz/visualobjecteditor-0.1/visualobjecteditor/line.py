from dataclasses import dataclass
from typing import Iterable, Iterator, Optional

from visualobjecteditor.base import Document, SerializationResult, T, VisualObjectEditor
from visualobjecteditor.table import TableFormatter


@dataclass(kw_only=True)
class LineObjectEditor(VisualObjectEditor[str, T]):
    id_divider: str = '|'
    lstrip_lines: bool = False
    rstrip_lines: bool = True
    ignore_empty_lines: bool = True

    @property
    def _table_formatter(self) -> TableFormatter:
        def cell_stripper(line: str, _column_id: int) -> str:
            if self.lstrip_lines:
                line = line.lstrip()
            if self.rstrip_lines:
                line = line.rstrip()
            return line

        return TableFormatter(
            column_divider=self.id_divider,
            cell_stripper=cell_stripper,
            max_columns=1,
            ignore_divider_in_last_column=True,
            ignore_empty_lines=self.ignore_empty_lines,
        )

    def build_documents(self, lines: Iterable[SerializationResult[str]]) -> Iterator[Document]:
        if self.tracking_mode:
            yield Document(
                lines=self._table_formatter.serialize_table_with_ids((row.object_id, [row.data]) for row in lines),
            )
        else:
            yield Document(lines=self._table_formatter.serialize_table([row.data] for row in lines))

    def split_documents(self, documents: Iterable[Document]) -> Iterator[tuple[Optional[str], str]]:
        for document in documents:
            if self.tracking_mode:
                for object_id, row in self._table_formatter.parse_rows_with_id(document.lines):
                    yield object_id, row[0]
            else:
                for row in self._table_formatter.parse_rows(document.lines):
                    yield None, row[0]
