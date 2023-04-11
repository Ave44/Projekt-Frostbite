from enum import Enum, auto


class State(Enum):
    NORMAL = auto()
    DAMAGED = auto()
    HEALED = auto()
    DEAD = auto()
