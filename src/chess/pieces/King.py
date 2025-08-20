from typing import Union
from src.chess.Kernel import *
from src.chess.pieces.Piece import Piece
from src.chess.Space import Space

class King(Piece):
    def __init__(self, color: str, space: Space):
        super().__init__(color, KING.NAME, KING.SYMB, space, self._move_function)
        self.in_check = False
        self.developed = False
        self.get_moves()
    
    def _move_function(self) -> None:
        self.in_check = False

    def get_castle_positions(self) -> list[list[Space]]:
        positions: list[list[Space]] = []
        castle_left_files: list[str] = [f for f in [ self.position.decrease_file(), self.position.decrease_file(2) ] if f is not None]
        castle_right_files: list[str] =[f for f in [ self.position.increase_file(), self.position.increase_file(2) ] if f is not None]
        positions.append([
            Space(castle_left_files[0], self.position.rank),
            Space(castle_left_files[1], self.position.rank)
        ])
        positions.append([
            Space(castle_right_files[0], self.position.rank),
            Space(castle_right_files[1], self.position.rank)
        ])
        return positions

    def get_neighboring_spaces(self) -> list[list[Space]]:
        positions: list[list[Space]] = []
        rank_list: list[Union[int,None]] = [
            self.position.rank,
            self.position.increase_rank(),
            self.position.decrease_rank()
            ]
        file_list: list[Union[str,None]] = [
            self.position.file,
            self.position.increase_file(),
            self.position.decrease_file()
        ]
        ranks: list[int] = [r for r in rank_list if r is not None]
        files: list[str] = [f for f in file_list if f is not None]
        for rank in ranks:
            for file in files:
                new_space = Space(file, rank)
                if new_space != self.position:
                    positions.append([new_space])
        if not self.developed:
            positions += self.get_castle_positions()
        return positions
    
    def get_moves(self) -> None:
        self.moves = self.get_neighboring_spaces()