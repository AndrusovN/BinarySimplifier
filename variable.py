from __future__ import annotations
from numerical import Numerical
from typing import *


class Variable(Numerical):
    name: str
    id: int

    def __init__(self, name: str):
        self.name = name
        self.id = -1

    def __eq__(self, other: Variable):
        return self.id == other.id and self.name == other.name

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id
