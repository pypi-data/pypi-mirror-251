from dataclasses import dataclass
from typing import Callable, Generic, Iterable, Optional, TypeVar

from visualobjecteditor.base import (
    Document,
    ObjectEditingResult,
    OriginalObject,
    ParseResult,
    S,
    SerializationResult,
    T,
    VisualObjectEditor,
)
from visualobjecteditor.block import BlockObjectEditor
from visualobjecteditor.page import PageObjectEditor

U = TypeVar('U')


@dataclass(kw_only=True)
class NestedObjectEditor(Generic[T]):
    nested_editor: VisualObjectEditor[S, U]
    get_nested_objects: Callable[[T], Iterable[U]]
    build_header: Callable[[T], list[str]] = lambda obj: []  # noqa: E731
    build_object_id: Callable[[T], Optional[str]] = lambda obj: None  # noqa: E731
    parse_nested_editing_result: Callable[[T, ObjectEditingResult[U]], T]

    tracking_mode: bool = True
    allow_additions: bool = False
    allow_deletions: bool = False

    def serialize(self, obj: T) -> SerializationResult[list[str]]:
        sub_editing_process = self.nested_editor.start_editing_process()

        header = self.build_header(obj)
        lines = next(sub_editing_process.create_documents(self.get_nested_objects(obj))).lines

        return SerializationResult(
            data=header + lines,
            object_id=self.build_object_id(obj),
            process=sub_editing_process,
            header_length=len(header),
        )

    def parse(self, lines: list[str], original_object: OriginalObject[T]) -> ParseResult[T]:
        lines = lines[original_object.serialization_context.header_length:]

        sub_editing_process = original_object.serialization_context.process
        sub_editing_result = sub_editing_process.parse_documents([Document(lines=lines)])

        return ParseResult(
            object=self.parse_nested_editing_result(original_object.object, sub_editing_result),
            sub_editing_result=sub_editing_result,
        )


@dataclass(kw_only=True)
class NestedBlockObjectEditor(NestedObjectEditor[T], BlockObjectEditor[T]):
    pass


@dataclass(kw_only=True)
class NestedPageObjectEditor(NestedObjectEditor[T], PageObjectEditor[T]):
    pass
