from dataclasses import dataclass, field
from sqlite3 import Row


@dataclass
class Block:

    row: Row

    children: list["Block"] = field(default_factory=list)
