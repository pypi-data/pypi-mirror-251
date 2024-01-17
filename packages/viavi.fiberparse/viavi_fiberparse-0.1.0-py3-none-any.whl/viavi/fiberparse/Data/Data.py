from abc import ABC
from dataclasses import dataclass


@dataclass(init=True, frozen=True)
class Data(ABC):
    def __init__(self):
        pass
