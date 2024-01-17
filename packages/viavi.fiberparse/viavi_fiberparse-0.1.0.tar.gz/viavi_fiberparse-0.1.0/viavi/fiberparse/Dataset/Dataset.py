from dataclasses import dataclass
from typing import List

from viavi.fiberparse.Data.Data import Data


@dataclass(init=True, frozen=True)
class Dataset:
    data: List[Data]
