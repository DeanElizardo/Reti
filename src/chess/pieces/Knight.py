from src.chess.Kernel import *
from src.chess.pieces.Piece import Piece
from src.chess.Space import Space

class Knight(Piece):
    def __init__(self, color: str, space: Space):
        super().__init__(color, KNIGHT.NAME, KNIGHT.SYMB, space, self._move_function)
        self.get_moves()

    def _move_function(self) -> None:
        pass

    def get_hops(self) -> list[list[Space]]:
        positions: list[list[Space]] = []
        advance_rank = self.position.increase_rank(2)
        decrease_rank = self.position.decrease_rank(2)
        advance_file = self.position.increase_file(2)
        decrease_file = self.position.decrease_file(2)
        
        if advance_rank is not None:
            hop_left = Space(self.position.file, advance_rank).decrease_file()
            hop_right = Space(self.position.file, advance_rank).increase_file()
            if hop_left is not None:
                positions.append([Space(hop_left, advance_rank)])
            if hop_right is not None:
                positions.append([Space(hop_right, advance_rank)])
        if decrease_rank is not None:
            hop_left = Space(self.position.file, decrease_rank).decrease_file()
            hop_right = Space(self.position.file, decrease_rank).increase_file()
            if hop_left is not None:
                positions.append([Space(hop_left, decrease_rank)])
            if hop_right is not None:
                positions.append([Space(hop_right, decrease_rank)])
        if advance_file is not None:
            hop_up = Space(advance_file, self.position.rank).increase_rank()
            hop_down = Space(advance_file, self.position.rank).decrease_rank()
            if hop_up is not None:
                positions.append([Space(advance_file, hop_up)])
            if hop_down is not None:
                positions.append([Space(advance_file, hop_down)])
        if decrease_file is not None:
            hop_up = Space(decrease_file, self.position.rank).increase_rank()
            hop_down = Space(decrease_file, self.position.rank).decrease_rank()
            if hop_up is not None:
                positions.append([Space(decrease_file, hop_up)])
            if hop_down is not None:
                positions.append([Space(decrease_file, hop_down)])
        return positions
    
    def get_moves(self) -> None:
        self.moves = self.get_hops()