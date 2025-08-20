from __future__ import annotations
from src.chess.Kernel import *
from typing import Union

class Space:
    def __init__(self, file: str, rank: int):
        self.file: str = file
        self.rank: int = rank

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Space):
            return False
        return self.file == other.file and self.rank == other.rank
    
    def __hash__(self) -> int:
        file_idx: int = self.get_file_integer(self.file)
        return hash((file_idx, self.rank))
    
    def __str__(self) -> str:
        return f"{self.file}{self.rank}"
    
    def clone(self) -> Space:
        return Space(self.file, self.rank)

    def increase_rank(self, distance: int = 1) -> Union[int, None]:
        if self.rank + distance <= max(BOARD_RANKS):
            return self.rank + distance
        else:
            return None
    
    def decrease_rank(self, distance: int = 1) -> Union[int, None]:
        if self.rank - distance >= min(BOARD_RANKS):
            return self.rank - distance
        else:
            return None
        
    def increase_file(self, distance: int = 1) -> Union[str, None]:
        file_index: int = self.get_file_integer(self.file)
        if file_index + distance < len(BOARD_FILES):
            return self.get_file_letter(file_index + distance)
        else:
            return None
        
    def decrease_file(self, distance: int = 1) -> Union[str, None]:
        file_index = self.get_file_integer(self.file)
        if file_index - distance >= 0:
            return self.get_file_letter(file_index - distance)
        else:
            return None
        
    def get_file_integer(self, file_letter: str) -> int:
        return BOARD_FILES.index(file_letter)
    
    def get_file_letter(self, file_integer: int) -> str:
        return BOARD_FILES[file_integer]