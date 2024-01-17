from dataclasses import dataclass
from typing import Iterable, Iterator, Optional

from visualobjecteditor.base import Document, SerializationResult, T, VisualObjectEditor


@dataclass(kw_only=True)
class PageObjectEditor(VisualObjectEditor[list[str], T]):

    def build_documents(self, pages: Iterable[SerializationResult[list[str]]]) -> Iterator[Document]:
        for page in pages:
            yield Document(lines=page.data, title=page.object_id if self.tracking_mode else None)

    def split_documents(self, documents: Iterable[Document]) -> Iterable[tuple[Optional[str], list[str]]]:
        for document in documents:
            yield document.title, document.lines
