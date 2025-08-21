from src.chess.Kernel import *
from src.chess.pieces.Piece import Piece
from src.chess.Space import Space

class Rook(Piece):
    def __init__(self, color: str, space: Space):
        super().__init__(color, ROOK, space, self._move_function)
        self.get_moves()

    def _move_function(self) -> None:
        pass

    def get_increasing_ranks(self) -> list[Space]:
        positions: list[Space] = []
        increasing_rank_position = self.position.increase_rank()
        while increasing_rank_position is not None:
            positions.append(
                Space(self.position.file, increasing_rank_position)
            )
            increasing_rank_position = positions[-1].increase_rank()
        return positions
    
    def get_decreasing_ranks(self) -> list[Space]:
        positions: list[Space] = []
        decreasing_rank_position = self.position.decrease_rank()
        while decreasing_rank_position is not None:
            positions.append(
                Space(self.position.file, decreasing_rank_position)
            )
            decreasing_rank_position = positions[-1].decrease_rank()
        return positions
    
    def get_increasing_files(self) -> list[Space]:
        positions: list[Space] = []
        increasing_file_position = self.position.increase_file()
        while increasing_file_position is not None:
            positions.append(
                Space(increasing_file_position, self.position.rank)
            )
            increasing_file_position = positions[-1].increase_file()
        return positions
    
    def get_decreasing_files(self) -> list[Space]:
        positions: list[Space] = []
        decreasing_file_position = self.position.decrease_file()
        while decreasing_file_position is not None:
            positions.append(
                Space(decreasing_file_position, self.position.rank)
            )
            decreasing_file_position = positions[-1].decrease_file()
        return positions

    def get_moves(self) -> None:
        positions: list[list[Space]] = []
        advance_rank_attack_lanes = self.get_increasing_ranks()
        decrease_rank_attack_lanes = self.get_decreasing_ranks()
        increase_file_attack_lanes = self.get_increasing_files()
        decrease_file_attack_lanes = self.get_decreasing_files()
        positions.append(advance_rank_attack_lanes)
        positions.append(decrease_rank_attack_lanes)
        positions.append(increase_file_attack_lanes)
        positions.append(decrease_file_attack_lanes)
        self.moves = positions