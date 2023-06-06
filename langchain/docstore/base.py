"""Interface to access to place that stores documents."""
import abc
from abc import ABC, abstractmethod
from typing import Dict, Union, Sequence, Iterator, Optional
from uuid import UUID

import dataclasses
from langchain.schema import Document


class Docstore(ABC):
    """Interface to access to place that stores documents."""

    @abstractmethod
    def search(self, search: str) -> Union[str, Document]:
        """Search for document.

        If page exists, return the page summary, and a Document object.
        If page does not exist, return similar entries.
        """


class AddableMixin(ABC):
    """Mixin class that supports adding texts."""

    @abstractmethod
    def add(self, texts: Dict[str, Document]) -> None:
        """Add more documents."""


@dataclasses.dataclass(frozen=True)
class Selector:
    """Selection criteria represented in conjunctive normal form.

    https://en.wikipedia.org/wiki/Conjunctive_normal_form

    At the moment, the explicit representation is used for simplicity / prototyping.

    It may be replaced by an ability of specifying selection with jq
    if operating on JSON metadata or else something free form like SQL.
    """

    parent_hashes: Optional[Sequence[UUID]] = None
    hashes: Optional[Sequence[UUID]] = None
    ids: Optional[Sequence[str]] = None


# @dataclasses.dataclass(frozen=True)
# class FreeFormSelector(BaseSelector):
#     # Some selector that matches syntax of underlying vector store
#     query: str
#     kwargs: Any


class ArtifactLayer(abc.ABC):
    """Use to keep track of artifacts generated while processing content.

    The first version of the artifact store is used to work with Documents
    rather than Blobs.

    We will likely want to evolve this into Blobs, but faster to prototype
    with Documents.
    """

    @abc.abstractmethod
    def exists(self, ids: Sequence[str]) -> Sequence[bool]:
        """Check if the artifacts with the given id exist."""

    # @abc.abstractmethod
    # def exist_by_hash(self, hashes: Sequence[str]) -> Sequence[bool]:
    #     """Check if the artifacts with the given hash exist."""
    #     raise NotImplementedError()

    def add(self, documents: Sequence[Document]) -> None:
        """Add the given artifacts."""
        raise NotImplementedError()

    def get_child_documents(self, hashes: Sequence[UUID]) -> Iterator[Document]:
        """Get the child documents of the given parent document."""
        yield from self.get_matching_documents(Selector(parent_hashes=hashes))

    def get_matching_documents(self, selector: Selector) -> Iterator[Document]:
        """Yield documents matching the given selector."""
        raise NotImplementedError()
