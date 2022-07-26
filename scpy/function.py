"""
    SitCalc is a library for doing stuff in Situation Calculus written in Python
    Copyright (C) 2022 Lukas Grassauer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    TODO: Write docstring for module
"""

from typing import Sequence, TypeAlias

from pydantic import Field
from pydantic.dataclasses import dataclass

_Function: TypeAlias = "Function"


@dataclass
class Function:
    """
    TODO: Write docstring for class
    """
    symbol: str
    arguments: Sequence[_Function] = Field(default_factory=tuple)
