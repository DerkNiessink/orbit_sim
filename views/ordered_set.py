"""Ordered set."""

from collections.abc import KeysView
from typing import Generic, Iterator, Sequence, TypeVar

T = TypeVar("T")


class OrderedSet(Generic[T]):
    """Ordered set with a maximum length."""

    def __init__(self, maxlen: int) -> None:
        self.__items: dict[T, None] = dict()  # We use the dict keys as an ordered set. Values are always None.
        self.__maxlen = maxlen

    def append(self, item: T) -> None:
        """Add one item and remove one item (on a first-in-first-out basis) if the set is too big."""
        self.__items[item] = None
        if len(self) > self.__maxlen:  # Remove one item
            for key in self.__items:
                del self.__items[key]
                break

    def extend(self, items: Sequence[T]) -> None:
        """Add multiple items and remove one or more items (on a first-in-first-out basis) if the set is too big."""
        for item in items:
            self.append(item)

    def items(self) -> KeysView[T]:
        """Return the items in the set."""
        return self.__items.keys()

    def clear(self) -> None:
        """Remove all items from the set."""
        self.__items.clear()

    def __len__(self) -> int:
        """Return the number of items in the set."""
        return len(self.__items)

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over all items in the set."""
        for key in self.__items:
            yield key
