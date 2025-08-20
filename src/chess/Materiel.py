from typing import Union
from src.chess.Kernel import *
from src.chess.Space import Space
from src.chess.pieces.Pawn import Pawn
from src.chess.pieces.Rook import Rook
from src.chess.pieces.Knight import Knight
from src.chess.pieces.Bishop import Bishop
from src.chess.pieces.Queen import Queen
from src.chess.pieces.King import King

PieceList = Union[
    list[King],
    list[Queen],
    list[Pawn],
    list[Rook],
    list[Knight],
    list[Bishop]
    ]

class Materiel:
    def __init__(self, color: str):
            first_rank: int = -1
            second_rank: int = -1
            king_file: str = ""
            queen_file: str = ""
            if color == BLACK:
                first_rank = 8
                second_rank = 7
                king_file = 'e'
                queen_file = 'd'
            else:
                first_rank = 1
                second_rank = 2
                king_file = 'e'
                queen_file = 'd'
            self.king: list[King] = [King(color, Space(king_file, first_rank))]
            self.queens: list[Queen] = [Queen(color, Space(queen_file, first_rank))]
            self.rooks: list[Rook] = [
                Rook(color, Space('a', first_rank)),
                Rook(color, Space('h', first_rank))
            ]
            self.knights: list[Knight] = [
                Knight(color, Space('b', first_rank)),
                Knight(color, Space('g', first_rank))
            ]
            self.bishops: list[Bishop] = [
                Bishop(color, Space('c', first_rank)),
                Bishop(color, Space('f', first_rank))
            ]
            self.pawns: list[Pawn] = [
                Pawn(color, Space('a', second_rank)),
                Pawn(color, Space('b', second_rank)),
                Pawn(color, Space('c', second_rank)),
                Pawn(color, Space('d', second_rank)),
                Pawn(color, Space('e', second_rank)),
                Pawn(color, Space('f', second_rank)),
                Pawn(color, Space('g', second_rank)),
                Pawn(color, Space('h', second_rank))
            ]
            self.iterable_collection: list[PieceList] = [
                self.king,
                self.queens,
                self.rooks,
                self.knights,
                self.bishops,
                self.pawns
            ]
            self._iter_idx = 0
    
    def __iter__(self):
        for group in self.iterable_collection:
            yield group