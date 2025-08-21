from __future__ import annotations
from typing import Callable
from src.chess.Space import Space
from src.chess.Kernel import PieceDescriptor

class Piece:
    def __init__(
            self, 
            color: str, 
            piece_descriptor: PieceDescriptor,
            space: Space,
            move_function: Callable[[], None]):
        self.color: str = color
        self.name: str = piece_descriptor.NAME
        self.symbol: str = piece_descriptor.SYMB
        self.points = piece_descriptor.POINTS
        self.position: Space = space
        self.developed: bool = False
        self.moves: list[list[Space]] = []
        self.pinned: bool = False
        self.checking: bool = False
        self._move_function = move_function
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return False
        prop_comparisons = [
            self.name == other.name,
            self.color == other.color,
            self.symbol == other.symbol,
            self.position == other.position
        ]
        return all(prop_comparisons)
    
    def __hash__(self) -> int:
        return hash((self.name, self.symbol, self.color, self.position))    
    
    def pin(self):
        self.pinned = True

    def unpin(self):
        self.pinned = False

    def check(self):
        self.checking = True

    def uncheck(self):
        self.checking = False
    
    def get_marker(self) -> str:
        return f"{self.symbol}{self.position.file}{self.position.rank}"
    
    def get_moves(self) -> None:
        raise Exception("get_moves() should be defined in a subclass")

    def move(self, space: Space) -> None:
        self.position = space
        self._move_function()
        self.developed |= True
        self.get_moves()
