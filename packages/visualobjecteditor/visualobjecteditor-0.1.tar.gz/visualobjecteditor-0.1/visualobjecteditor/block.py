import re
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Iterator, Optional

from visualobjecteditor.base import Document, InvalidSerializationError, SerializationResult, T, VisualObjectEditor
from visualobjecteditor.utils import join_with_empty_line, split_on_empty_lines


@dataclass(kw_only=True)
class BlockObjectEditor(VisualObjectEditor[list[str], T]):
    separator_line_count: int = 1
    id_divider: str = '|'

    @cached_property
    def _id_divider_pattern(self) -> re.Pattern:
        return re.compile(fr'{re.escape(self.id_divider)}\s?')

    def _build_block(self, block: SerializationResult[list[str]]) -> Iterator[str]:
        if not block.data:
            raise InvalidSerializationError("Serialized block is empty.")

        for line_number, line in enumerate(block.data):
            if '\n' in line:
                raise InvalidSerializationError("Line in a serialized block contains a line break.")
            if not line.strip():
                raise InvalidSerializationError("Serialized block contains an empty line.")

            if self.tracking_mode and line_number == 0:
                yield f"{block.object_id} {self.id_divider} {line}"
            else:
                yield line

    def build_documents(self, blocks: Iterable[SerializationResult[list[str]]]) -> Iterator[Document]:
        yield Document(lines=list(join_with_empty_line(
            line_groups=(self._build_block(block) for block in blocks),
            empty_line_count=self.separator_line_count,
        )))

    def split_documents(self, documents: Iterable[Document]) -> Iterable[tuple[Optional[str], list[str]]]:
        for document in documents:
            for block_lines in split_on_empty_lines(document.lines):
                if self.tracking_mode:
                    id_string, block_lines[0] = self._id_divider_pattern.split(block_lines[0], maxsplit=1)
                    yield id_string, block_lines
                else:
                    yield None, block_lines
