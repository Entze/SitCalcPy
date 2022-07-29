from collections import defaultdict
from typing import TypeVar, MutableMapping, Set, Any, Optional, Tuple

_T = TypeVar('_T')
_U = TypeVar('_U')



#class Relation:
#
#    def __init__(self, initial_mapping:Optional[Tuple[]]):
#        self.__internal_mapping: MutableMapping[_T, Set[_U]] = defaultdict(lambda: set())
#
#    def relate(self, r1: _T, r2: _U):
#        self.__internal_mapping[r1].add(r2)
