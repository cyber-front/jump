from dataclasses import dataclass

@dataclass
class Move:
    move_loc: int
    jump_loc: int
    rest_loc: int

