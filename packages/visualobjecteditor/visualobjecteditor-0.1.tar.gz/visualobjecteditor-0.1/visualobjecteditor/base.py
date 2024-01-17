import contextlib
import os
import shlex
import subprocess
import tempfile
from abc import ABC, abstractmethod
from contextlib import ExitStack
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Callable, Generic, Iterable, Iterator, Optional, TypeVar, Union

from visualobjecteditor.utils import get_fullscreen_choice


@dataclass
class Document:
    lines: list[str]
    title: Optional[str] = None


S = TypeVar("S")  # serialization result type

T = TypeVar("T")  # object type


class InvalidSerializationError(Exception):
    pass


class ObjectEditingError(Exception):
    pass


class ParseError(ObjectEditingError):
    pass


class ObjectAddedError(ObjectEditingError):

    def __init__(self):
        super().__init__("Objects may not be created.")


class ObjectDeletedError(ObjectEditingError):

    def __init__(self):
        super().__init__("Objects may not be deleted.")


class ObjectReorderedError(ObjectEditingError):

    def __init__(self):
        super().__init__("Objects may not be reordered.")


class OperationCancelledError(Exception):
    def __init__(self):
        super().__init__("Editing process cancelled by user.")


class Operation(ABC):

    @abstractmethod
    def is_change(self) -> bool:
        raise NotImplementedError()


@dataclass
class Addition(Operation, Generic[T]):
    added_object: T
    meta: SimpleNamespace

    def is_change(self) -> bool:
        return True


@dataclass
class Deletion(Operation, Generic[T]):
    deleted_object: T

    def is_change(self) -> bool:
        return True


@dataclass
class Update(Operation, Generic[T]):
    original_object: T
    new_object: T
    meta: SimpleNamespace

    def is_change(self) -> bool:
        return self.original_object != self.new_object


@dataclass
class UnknownOperation(Operation, Generic[T]):
    new_object: T
    meta: SimpleNamespace

    def is_change(self) -> bool:
        return True


@dataclass
class ObjectEditingResult(Generic[T]):
    has_reordered_objects: bool = False

    _operations: list[Operation] = field(default_factory=list)
    _update_map: dict[T, Optional[T]] = field(default_factory=dict)
    _reverse_update_map: dict[T, Optional[T]] = field(default_factory=dict)

    def add_operation(self, operation: Operation):
        self._operations.append(operation)

        if isinstance(operation, Update):
            with contextlib.suppress(TypeError):
                self._update_map[operation.original_object] = operation.new_object
            with contextlib.suppress(TypeError):
                self._reverse_update_map[operation.new_object] = operation.original_object

        if isinstance(operation, Deletion):
            with contextlib.suppress(TypeError):
                self._update_map[operation.deleted_object] = None

        if isinstance(operation, Addition):
            with contextlib.suppress(TypeError):
                self._reverse_update_map[operation.added_object] = None

    @property
    def operations(self) -> Iterator[Operation]:
        yield from self._operations

    @property
    def number_of_operations(self) -> int:
        return len(self._operations)

    @property
    def changes(self) -> Iterator[Operation]:
        for operation in self._operations:
            if operation.is_change():
                yield operation

    @property
    def number_of_changes(self) -> int:
        return sum(1 for _ in self.changes)

    @property
    def additions(self) -> Iterator[Addition]:
        for operation in self._operations:
            if isinstance(operation, Addition):
                yield operation

    @property
    def added_objects(self) -> Iterator[T]:
        for addition in self.additions:
            yield addition.added_object

    @property
    def number_of_additions(self) -> int:
        return sum(1 for _ in self.additions)

    @property
    def has_additions(self) -> bool:
        for _ in self.additions:
            return True
        return False

    @property
    def deletions(self) -> Iterator[Deletion]:
        for operation in self._operations:
            if isinstance(operation, Deletion):
                yield operation

    @property
    def deleted_objects(self) -> Iterator[T]:
        for deletion in self.deletions:
            yield deletion.deleted_object

    @property
    def number_of_deletions(self) -> int:
        return sum(1 for _ in self.deletions)

    @property
    def has_deletions(self) -> bool:
        for _ in self.deletions:
            return True
        return False

    @property
    def updates(self) -> Iterator[Update]:
        for operation in self._operations:
            if isinstance(operation, Update):
                yield operation

    @property
    def updated_objects(self) -> Iterator[T]:
        for update in self.updates:
            yield update.new_object

    @property
    def number_of_updates(self) -> int:
        return sum(1 for _ in self.updates)

    @property
    def has_updates(self) -> bool:
        for _ in self.updates:
            return True
        return False

    @property
    def modifications(self) -> Iterator[Update]:
        for operation in self._operations:
            if isinstance(operation, Update) and operation.is_change():
                yield operation

    @property
    def modified_objects(self) -> Iterator[T]:
        for modification in self.modifications:
            yield modification.new_object

    @property
    def number_of_modifications(self) -> int:
        return sum(1 for _ in self.modifications)

    @property
    def has_modifications(self) -> bool:
        for _ in self.modifications:
            return True
        return False

    @property
    def non_modifications(self) -> Iterator[Update]:
        for operation in self._operations:
            if isinstance(operation, Update) and not operation.is_change():
                yield operation

    @property
    def unmodified_objects(self) -> Iterator[T]:
        for modification in self.non_modifications:
            yield modification.new_object

    @property
    def number_of_unmodified_objects(self) -> int:
        return sum(1 for _ in self.non_modifications)

    @property
    def has_unmodified_objects(self) -> bool:
        for _ in self.non_modifications:
            return True
        return False

    def has_change(self) -> bool:
        return any(operation.is_change() for operation in self.operations) or self.has_reordered_objects

    def __iter__(self):
        for operation in self._operations:
            if isinstance(operation, Addition):
                yield operation.added_object
            if isinstance(operation, Update):
                yield operation.new_object
            if isinstance(operation, UnknownOperation):
                yield operation.new_object

    def __getitem__(self, index: Union[int, T]) -> Optional[T]:
        if isinstance(index, int):
            operation = self._operations[index]

            if isinstance(operation, Addition):
                return operation.added_object
            if isinstance(operation, Update):
                return operation.new_object
            if isinstance(operation, UnknownOperation):
                return operation.new_object
        else:
            if index in self._update_map:
                return self._update_map[index]

        raise IndexError()

    def __contains__(self, item):
        return any(item == obj for obj in self)

    def __len__(self):
        return sum(1 for _ in self)


@dataclass
class SerializationResult(Generic[S]):
    data: S
    object_id: Optional[str]
    context: SimpleNamespace

    def __init__(self, data: S, object_id: Optional[str] = None, **context):
        self.data = data
        self.object_id = object_id
        self.context = SimpleNamespace(**context)


@dataclass
class OriginalObject(Generic[T]):
    object: T
    serialization_context: SimpleNamespace


@dataclass
class ParseResult(Generic[T]):
    object: T
    meta: SimpleNamespace

    def __init__(self, object: T, **context):  # noqa: A002
        self.object = object
        self.meta = SimpleNamespace(**context)


@dataclass
class ObjectEditingProcess(Generic[T]):
    editor: 'VisualObjectEditor'

    original_objects_by_id: Optional[dict[str, OriginalObject[T]]] = field(init=False, default=None)
    indices_by_id: Optional[dict[str, int]] = field(init=False, default=None)

    def create_documents(self, objects: Iterable[T]) -> Iterator[Document]:
        if self.original_objects_by_id is not None or self.indices_by_id is not None:
            raise RuntimeError()

        self.original_objects_by_id = {}
        self.indices_by_id = {}
        serialization_results = []

        for i, obj in enumerate(objects, start=1):
            serialization_result = self.editor.serialize(obj)

            if not isinstance(serialization_result, SerializationResult):
                serialization_result = SerializationResult(serialization_result)

            if serialization_result.object_id is None:
                serialization_result.object_id = str(i)

            self.original_objects_by_id[serialization_result.object_id] = OriginalObject(
                object=obj,
                serialization_context=serialization_result.context,
            )

            self.indices_by_id[serialization_result.object_id] = i

            serialization_results.append(serialization_result)

        if len(self.original_objects_by_id) != len(serialization_results):
            raise InvalidSerializationError("Could not generate unique IDs.")

        if any(not s.strip() for s in self.original_objects_by_id):
            raise InvalidSerializationError("IDs must not be empty strings.")

        return self.editor.build_documents(serialization_results)

    def parse_documents(self, documents: Iterable[Document]) -> ObjectEditingResult:
        split_documents = self.editor.split_documents(documents)

        result = ObjectEditingResult()

        if self.editor.tracking_mode:
            visited_object_ids = set()

            last_obj_index = -1
            for object_id, text_unit in split_documents:
                object_id = object_id.strip()

                if object_id:
                    if object_id in visited_object_ids:
                        raise ObjectEditingError(f"The object ID {object_id} appears twice.")
                    else:
                        visited_object_ids.add(object_id)

                    try:
                        original_object = self.original_objects_by_id[object_id]
                    except KeyError as err:
                        raise ObjectEditingError(f"The object ID {object_id} does not exist.") from err
                else:
                    original_object = None

                    if not self.editor.allow_additions:
                        raise ObjectAddedError()

                parse_result = self.editor.parse(text_unit, original_object=original_object)

                if not isinstance(parse_result, ParseResult):
                    parse_result = ParseResult(object=parse_result)

                if object_id:
                    result.add_operation(Update(
                        original_object=original_object.object,
                        new_object=parse_result.object,
                        meta=parse_result.meta,
                    ))

                    if not result.has_reordered_objects:
                        if self.indices_by_id[object_id] <= last_obj_index:
                            result.has_reordered_objects = True

                            if not self.editor.allow_reordering:
                                raise ObjectReorderedError()
                        else:
                            last_obj_index = self.indices_by_id[object_id]
                else:
                    result.add_operation(Addition(
                        added_object=parse_result.object,
                        meta=parse_result.meta,
                    ))

            missing_ids = set(self.original_objects_by_id.keys()) - visited_object_ids

            if missing_ids and not self.editor.allow_deletions:
                raise ObjectDeletedError()

            for object_id in missing_ids:
                result.add_operation(Deletion(self.original_objects_by_id[object_id].object))

        else:
            for _, text_unit in split_documents:
                parse_result = self.editor.parse(text_unit, original_object=None)

                if not isinstance(parse_result, ParseResult):
                    parse_result = ParseResult(object=parse_result)

                result.add_operation(UnknownOperation(
                    new_object=parse_result.object,
                    meta=parse_result.meta,
                ))

            if len(result) > len(self.original_objects_by_id) and not self.editor.allow_additions:
                raise ObjectAddedError()

            if len(result) < len(self.original_objects_by_id) and not self.editor.allow_deletions:
                raise ObjectDeletedError()

        return result


@dataclass(kw_only=True)
class VisualObjectEditor(Generic[S, T], ABC):
    editor: Optional[str] = None

    serializer: Optional[Callable[[T], Union[S, SerializationResult[S]]]] = None
    parser: Optional[Callable[[S, Optional[OriginalObject[T]]], Union[T, ParseResult[T]]]] = None

    tracking_mode: bool = False
    allow_additions: bool = True
    allow_deletions: bool = True
    allow_reordering: bool = True

    skip_lines_starting_with: Optional[str] = '#'
    header: list[str] = field(default_factory=list)
    footer: list[str] = field(default_factory=list)

    allow_retry_on_failure: bool = True
    ask_for_confirmation_on_success: bool = False

    def __post_init__(self):
        # Try to find editor if not given
        for env_variable in ('VISUAL_OBJECT_EDITOR', 'VISUAL', 'EDITOR'):
            if not self.editor:
                self.editor = os.environ.get(env_variable)
        if not self.editor:
            raise ValueError("No editor specified")

    def serialize(self, obj: T) -> Union[S, SerializationResult[S]]:
        return self.serializer(obj)

    def parse(self, text_unit: S, original_object: Optional[OriginalObject[T]]) -> Union[T, ParseResult[T]]:
        return self.parser(text_unit, original_object)

    @abstractmethod
    def build_documents(self, serialization_results: Iterable[SerializationResult[S]]) -> Iterator[Document]:
        raise NotImplementedError()

    @abstractmethod
    def split_documents(self, documents: Iterable[Document]) -> Iterator[tuple[Optional[str], S]]:
        raise NotImplementedError()

    def edit_documents(self, documents: Iterable[Document]) -> Iterator[Document]:
        with ExitStack() as stack:
            tmpdir = Path(stack.enter_context(tempfile.TemporaryDirectory()))

            tmp_files = []

            for n, document in enumerate(documents, start=1):
                title = str(n) if document.title is None else document.title

                tmp_file = stack.enter_context((tmpdir / title).open('w+'))
                for line in self.header:
                    tmp_file.write(f"{self.skip_lines_starting_with} {line}\n")
                for line in document.lines:
                    tmp_file.write(f"{line}\n")
                for line in self.footer:
                    tmp_file.write(f"{self.skip_lines_starting_with} {line}\n")
                tmp_file.flush()

                tmp_files.append(tmp_file)

            if not tmp_files:
                return []

            result = subprocess.run(
                args=(
                    *(shlex.split(self.editor)),
                    *(tmp_file.name for tmp_file in tmp_files),
                ),
                shell=False,
            )

            if result.returncode:
                raise ObjectEditingError(f"Return code of editor was {result.returncode}.")
            else:
                for tmp_file in tmp_files:
                    tmp_file.seek(0)
                    yield Document(
                        lines=[
                            line.rstrip('\n')
                            for line in tmp_file
                            if not line.startswith(self.skip_lines_starting_with)
                        ],
                        title=Path(tmp_file.name).name,
                    )

    def get_success_message(self, result: ObjectEditingResult) -> str:
        if self.tracking_mode:
            if result.has_change():
                return (
                    "[bold]Success:[/bold] "
                    f"You've made [magenta]{result.number_of_modifications}[/magenta] modifications, "
                    f"[magenta]{result.number_of_additions}[/magenta] additions "
                    f"and [magenta]{result.number_of_deletions}[/magenta] deletions."
                )
            else:
                return (
                    "[bold]Success:[/bold] You've made no changes."
                )
        else:
            return f"Your changes are valid. They contain {len(result)} objects."

    def get_error_message(self, error: ObjectEditingError) -> str:
        return f"[bold magenta]Error:[/bold magenta] {error}"

    def start_editing_process(self) -> ObjectEditingProcess:
        return ObjectEditingProcess(self)

    def edit(self, objects: Iterable[T]) -> ObjectEditingResult:
        process = self.start_editing_process()
        original_documents = list(process.create_documents(objects))
        documents = original_documents

        while True:
            try:
                documents = list(self.edit_documents(documents))
                result = process.parse_documents(documents)

                if self.ask_for_confirmation_on_success:
                    key = get_fullscreen_choice(
                        self.get_success_message(result),
                        title="Confirm",
                        border_style="blue",
                        choices={
                            'Y': "Accept changes",
                            'E': "Continue editing",
                            'R': "Reset and edit again",
                            'X': "Cancel",
                        },
                    )

                    if key == 'E':
                        continue
                    elif key == 'R':
                        documents = original_documents
                        continue
                    elif key == 'X':
                        raise OperationCancelledError()

                return result

            except ObjectEditingError as err:
                if self.allow_retry_on_failure:
                    key = get_fullscreen_choice(
                        self.get_error_message(err),
                        title="Error",
                        border_style="red",
                        choices={
                            'E': "Continue editing",
                            'R': "Reset and edit again",
                            'X': "Cancel",
                        },

                    )

                    if key == 'E':
                        continue
                    elif key == 'R':
                        documents = original_documents
                        continue
                    elif key == 'X':
                        raise OperationCancelledError() from err
                else:
                    raise err
