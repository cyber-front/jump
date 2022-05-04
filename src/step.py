from dataclasses import dataclass
import typing
import move

State = typing.Set[int]

@dataclass
class Step:
    start_state: State
    transition: move.Move
    final_state: State