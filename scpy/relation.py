from typing import Optional, TypeAlias, Mapping, Collection, MutableMapping, Set, Iterable, Any, Tuple, Union

from frozendict import frozendict  # type: ignore

from scpy.primitives import Function

_Relation: TypeAlias = 'Relation'


class Relation:

    def __init__(self, relation: Union[_Relation, Mapping[Function, Collection[Function]], None] = None):
        if relation is None:
            self._relation: Mapping[Function, Collection[Function]] = frozendict()
        elif isinstance(relation, Relation):
            self._relation = frozendict({key: frozenset(value) for key, value in relation._relation.items()})
        else:
            assert isinstance(relation, Mapping)
            self._relation = frozendict({key: frozenset(value) for key, value in relation.items()})

    @classmethod
    def from_tuples(cls, *tuples: Tuple[Function, Function]):
        relation_mapping: MutableMapping[Function, Set[Function]] = {}
        for t in tuples:
            relation_mapping.setdefault(t[0], set()).add(t[1])
        relation = cls.__new__(cls)
        super(Relation, relation).__init__(relation_mapping)
        return relation

    def __hash__(self) -> int:
        return hash(('Relation', self._relation))

    def __str__(self) -> str:
        return f"{'{'}{', '.join(f'{key}<>{value}' for key, values in self._relation.items() for value in values)}{'}'}"

    def __getitem__(self, item: Any) -> Iterable[Function]:
        return self._relation.get(item, ())

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
