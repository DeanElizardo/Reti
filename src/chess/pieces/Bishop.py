from src.chess.Kernel import *
from src.chess.pieces.Piece import Piece
from src.chess.Space import Space

class Bishop(Piece):
    def __init__(self, color: str, space: Space):
        super().__init__(color, BISHOP.NAME, BISHOP.SYMB, space, self._move_function)
        self.get_moves()
    
    def _move_function(self) -> None:
        pass

    def advance_rank_increase_file_diag(self) -> list[Space]:
        positions: list[Space] = []
        advance_rank = self.position.increase_rank()
        increase_file = self.position.increase_file()
        while advance_rank is not None and increase_file is not None:
            new_space = Space(increase_file, advance_rank)
            positions.append(new_space)
            advance_rank = new_space.increase_rank()
            increase_file = new_space.increase_file()
        return positions
    
    def advance_rank_decrease_file_diag(self) -> list[Space]:
        positions: list[Space] = []
        advance_rank = self.position.increase_rank()
        decrease_file = self.position.decrease_file()
        while advance_rank is not None and decrease_file is not None:
            new_space = Space(decrease_file, advance_rank)
            advance_rank = new_space.increase_rank()
            decrease_file = new_space.decrease_file()
        return positions
    
    def decrease_rank_increase_file_diag(self) -> list[Space]:
        positions: list[Space] = []
        decrease_rank = self.position.decrease_rank()
        increase_file = self.position.increase_file()
        while decrease_rank is not None and increase_file is not None:
            new_space = Space(increase_file, decrease_rank)
            positions.append(new_space)
            decrease_rank = new_space.decrease_rank()
            increase_file = new_space.increase_file()
        return positions
    
    def decrease_rank_decrease_file_diag(self) -> list[Space]:
        positions: list[Space] = []
        decrease_rank = self.position.decrease_rank()
        decrease_file = self.position.decrease_file()
        while decrease_rank is not None and decrease_file is not None:
            new_space = Space(decrease_file, decrease_rank)
            positions.append(new_space)
            decrease_rank = new_space.decrease_rank()
            decrease_file = new_space.decrease_file()
        return positions

    def get_moves(self) -> None:
        self.moves = []
        self.moves.append(self.advance_rank_increase_file_diag())
        self.moves.append(self.advance_rank_decrease_file_diag())
        self.moves.append(self.decrease_rank_increase_file_diag())
        self.moves.append(self.decrease_rank_decrease_file_diag())