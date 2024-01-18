from typing import Any, Iterable, Optional, Callable

from typing import TypeVar

I = TypeVar('I')
R = TypeVar('R')


class BaseIteratorPrinter:
    def print(self,
              iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None,
              decimal_as: str = 'string',
              sort_keys: bool = True):
        raise NotImplementedError()
