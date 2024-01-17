"""This module contains the Tag interface and the related StringTag extension."""

from abc import abstractmethod

from dataclasses import dataclass


class Tag:
    """ A general interface for a tag."""

    @property
    @abstractmethod
    def value(self) -> object:
        """Returns the tag value."""
        pass


@dataclass(frozen=True, unsafe_hash=True)
class StringTag(Tag):
    """
    A string tag associated to a BabelSynset.
    """

    tag: str
    """The string tag"""

    @property
    def value(self) -> str:
        return self.tag


@dataclass(frozen=True, unsafe_hash=True)
class LabelTag(Tag):
    """
    A label tag associated to a BabelSynset.
    """

    language: 'babelnet.language.Language'
    """The language of the tag"""

    label: str
    """The string tag"""

    @property
    def value(self) -> str:
        return self.label

    def __repr__(self):
        return f"{self.language}:{self.label}"
