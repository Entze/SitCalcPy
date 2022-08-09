from typing import TypeAlias, Optional, Mapping, Collection, Set, MutableMapping, Tuple, Union, Any, Iterator

from frozendict import frozendict  # type: ignore

from scpy.primitives import Function

_Preorder: TypeAlias = 'Preorder'


class Preorder:

    def __init__(self, __object: Union[_Preorder, Mapping[Function, Collection[Function]], None] = None):
        if __object is None:
            self._relation: Mapping[Function, Collection[Function]] = frozendict()
        elif isinstance(__object, Preorder):
            self._relation = frozendict({key: frozenset(value) for key, value in __object._relation.items()})
        else:
            assert isinstance(__object, Mapping)
            self._relation = frozendict({key: frozenset(value) for key, value in __object.items()})

    @classmethod
    def from_tuples(cls, *tuples: Tuple[Function, Function],
                    transitivity: bool = False,
                    symmetry: bool = False,
                    reflexivity: bool = False) -> _Preorder:
        relation_mapping: MutableMapping[Function, Set[Function]] = {}
        for t in tuples:
            a, b = t
            relation_mapping.setdefault(a, set()).add(b)
            if symmetry:
                relation_mapping.setdefault(b, set()).add(a)
            if reflexivity:
                assert a in relation_mapping
                relation_mapping[a].add(a)
                relation_mapping.setdefault(b, set()).add(b)

        if transitivity:
            changed = True
            while changed:
                changed = False
                for a, bs in relation_mapping.items():
                    add_to_a: Set[Function] = set()
                    for b in bs:
                        for c in relation_mapping.get(b, ()):
                            add_to_a.add(c)
                    assert a in relation_mapping
                    relation_mapping[a].update(add_to_a)
                    if symmetry:
                        for c in add_to_a:
                            if c not in add_to_a:
                                relation_mapping.setdefault(c, set()).add(a)
                                changed = True

        relation = cls.__new__(cls)
        super(Preorder, relation).__init__()
        relation._relation = relation_mapping
        return relation

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

    def __getitem__(self, item: Any) -> Iterator[Function]:
        if isinstance(item, Function):
            yield from self.get(item)

    def get(self, item: Function) -> Iterator[Function]:
        yield from self._relation.get(item, ())

    def get_inv(self, item: Function) -> Iterator[Function]:
        return (elem for elem, relates in self._relation if item in relates)

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
