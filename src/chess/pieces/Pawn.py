from typing import Union
from src.chess.Kernel import *
from src.chess.pieces.Piece import Piece
from src.chess.Space import Space

class Pawn(Piece):
    def __init__(self, color: str, space: Space):
        super().__init__(color, PAWN, space, self._move_function)
        self.get_moves()
        (self.passant_armed,
         self.passant_vuln,
         self.passant_attack_rank,
         self.passant_vuln_rank) = self.init_en_passant()
        
    def _move_function(self) -> None:
        self.passant_armed = self.position.rank == self.passant_attack_rank
        self.passant_vuln = not self.developed and self.position.rank == self.passant_vuln_rank
        
    def advance_position(self) -> list[list[Space]]:
        position: list[list[Space]] = []
        new_rank: Union[int, None] = None
        if self.color == BLACK:
            new_rank = self.position.decrease_rank()
        elif self.color == WHITE:
            new_rank = self.position.increase_rank()
        if new_rank is not None:
            position.append(
                [Space(self.position.file, new_rank)]
            )
        if not self.developed:
            alternate_rank = None
            if self.color == BLACK:
                alternate_rank = self.position.decrease_rank(distance=2)
            elif self.color == WHITE:
                alternate_rank = self.position.increase_rank(distance=2)
            if alternate_rank is not None:
                position.append(
                    [Space(self.position.file, alternate_rank)]
                )
        return position
    
    def capture_positions(self) -> list[list[Space]]:
        positions: list[list[Space]] = []
        advanced_positions: list[list[Space]] = self.advance_position()
        if len(advanced_positions) > 0:
            for attack_lane in advanced_positions:
                for advanced_position in attack_lane:
                    lesser_file: Union[str, None] = advanced_position.decrease_file()
                    greater_file: Union[str, None] = advanced_position.increase_file()
                    if lesser_file is not None:
                        positions.append(
                            [Space(lesser_file, advanced_position.rank)]
                        )
                    if greater_file is not None:
                        positions.append(
                            [Space(greater_file, advanced_position.rank)]
                        )
        return positions
    
    def init_en_passant(self):
        rank = self.position.rank
        attack_rank = rank
        vuln_rank = rank
        if self.color == 'black':
            attack_rank = self.position.decrease_rank(distance=3)
            vuln_rank = self.position.decrease_rank(distance=2)
        elif self.color == 'white':
            attack_rank = self.position.increase_rank(distance=3)
            vuln_rank = self.position.increase_rank(distance=2)
        return (
            False,
            False,
            attack_rank,
            vuln_rank
        )
    
    def get_moves(self) -> None:
        self.moves = self.advance_position() + self.capture_positions()