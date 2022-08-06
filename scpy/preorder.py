from typing import TypeAlias, Optional, Mapping, Collection, Set, MutableMapping

from frozendict import frozendict  # type: ignore

from scpy.function.function import Function

_Preorder: TypeAlias = 'Preorder'


class Preorder:

    def __init__(self, tp: Optional[_Preorder] = None):
        if tp is None:
            self._relation: Mapping[Function, Collection[Function]] = frozendict()
        else:
            self._relation = frozendict({key: frozenset(value) for key, value in tp._relation.items()})

    def __hash__(self) -> int:
        return hash(('Preorder', self._relation))

    def __str__(self) -> str:
        similar = {(key, value) for key, values in self._relation.items() for value in values if
                   self.is_preceded(value, key)}
        strictly = {(key, value) for key, values in self._relation.items() for value in values if
                    not self.is_preceded(value, key)}
        elems = (*(f'{key} ⪯ {value}' for key, values in self._relation.items() for value in values
                   if (key, value) not in similar and (key, value) not in strictly),
                 *(f'{key} ≺ {value}' for (key, value) in strictly),
                 *(f'{key} ~ {value}' for (key, value) in similar if (key, value) <= (value, key)))
        return f"{'{'}{', '.join(elems)}{'}'}"

    def is_preceded(self, left: Function, right: Function) -> bool:
        return right in self._relation.get(left, ())

    def is_similar(self, left: Function, right: Function) -> bool:
        return self.is_preceded(left, right) and self.is_preceded(right, left)

    def is_strictly_preceded(self, left: Function, right: Function) -> bool:
        return self.is_preceded(left, right) and not self.is_preceded(right, left)


class MutablePreorder(Preorder):

    def __init__(self, tp: Optional[Preorder] = None):
        super().__init__(tp)
        self._relation: MutableMapping[Function, Set[Function]] = {}
        if tp is not None:
            for key, value in tp._relation.items():
                self._relation[key] = set(value)

    def precedes(self, left: Function, right: Function) -> None:
        self._relation.setdefault(left, set()).add(right)
