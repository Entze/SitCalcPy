from typing import Optional, TypeAlias, Mapping, Collection, MutableMapping, Set

from frozendict import frozendict  # type: ignore

from scpy.primitives import Function

_Relation: TypeAlias = 'Relation'


class Relation:

    def __init__(self, relation: Optional[_Relation] = None):
        if relation is None:
            self._relation: Mapping[Function, Collection[Function]] = frozendict()
        else:
            self._relation = frozendict({key: frozenset(value) for key, value in self._relation.items()})

    def __hash__(self) -> int:
        return hash(('Relation', self._relation))

    def __str__(self) -> str:
        return f"{'{'}{', '.join(f'{key}<>{value}' for key, values in self._relation.items() for value in values)}{'}'}"

    def is_related(self, left: Function, right: Function) -> bool:
        return right in self._relation.get(left, ())


class MutableRelation(Relation):

    def __init__(self, relation: Optional[Relation] = None):
        super().__init__()
        if relation is None:
            self._relation: MutableMapping[Function, Set[Function]] = {}
        else:
            self._relation = {key: set(value) for key, value in self._relation.items()}

    def relates(self, left: Function, right: Function) -> None:
        self._relation.setdefault(left, set()).add(right)
