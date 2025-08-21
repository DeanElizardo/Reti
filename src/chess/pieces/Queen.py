from src.chess.Kernel import *
from src.chess.pieces.Piece import Piece
from src.chess.Space import Space
from src.chess.pieces.Rook import Rook
from src.chess.pieces.Bishop import Bishop

class Queen(Piece):
    def __init__(self, color: str, space: Space):
        super().__init__(color, QUEEN, space, self._move_function)
        self.get_moves()

    def _move_function(self) -> None:
        pass

    def get_rooklike_moves(self) -> list[list[Space]]:
        temp_rook = Rook(self.color, self.position)
        positions = [m for m in temp_rook.moves]
        del temp_rook
        return positions

    def get_bishoplike_moves(self) -> list[list[Space]]:
        temp_bishop = Bishop(self.color, self.position)
        positions = [m for m in temp_bishop.moves]
        del temp_bishop
        return positions
    
    def get_moves(self) -> None:
        self.moves = self.get_rooklike_moves() + self.get_bishoplike_moves()