import unittest
from src.chess.pieces.Bishop import Bishop
from src.chess.Kernel import *
from src.chess.Space import Space

class TestBishop(unittest.TestCase):
    def bishop_factory(self, color: str, space: Space) -> Bishop:
        return Bishop(color, space)
    
    def make_white_bishop(self, space: Space) -> Bishop:
        return self.bishop_factory(WHITE, space)
    
    def make_black_bishop(self, space: Space) -> Bishop:
        return self.bishop_factory(BLACK, space)
    
    def generate_all_spaces(self) -> list[Space]:
        all_spaces: list[Space] = []
        for file in BOARD_FILES:
            for rank in BOARD_RANKS:
                all_spaces.append(Space(file, rank))
        return all_spaces
    
    def generate_expected_spaces(self, init_space: Space) -> list[Space]:
        expected_spaces: list[Space] = []
        s = Space(init_space.file, init_space.rank)
        while s.increase_file() is not None and s.increase_rank() is not None:
            s = Space(s.increase_file(), s.increase_rank())
            expected_spaces.append(s)
        s = Space(init_space.file, init_space.rank)
        while s.increase_file() is not None and s.decrease_rank() is not None:
            s = Space(s.increase_file(), s.decrease_rank())
            expected_spaces.append(s)
        s = Space(init_space.file, init_space.rank)
        while s.decrease_file() is not None and s.increase_rank() is not None:
            s = Space(s.decrease_file(), s.increase_rank())
            expected_spaces.append(s)
        s = Space(init_space.file, init_space.rank)
        while s.decrease_file() is not None and s.decrease_rank() is not None:
            s = Space(s.decrease_file(), s.decrease_rank())
            expected_spaces.append(s)
        expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))
        return expected_spaces
    
    def white_bishop_has_right_moves(self, init_space: Space, expected_spaces: list[Space]):
        bishop = self.make_white_bishop(init_space)
        actual_spaces: list[Space] = []
        for m in bishop.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces= sorted(actual_spaces, key=lambda p: (p.file, p.rank))

        assert len(actual_spaces) == len(expected_spaces)

        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]

    def test_white_bishop(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            init_space = Space('c', 1)
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space)
            self.white_bishop_has_right_moves(init_space, expected_spaces)

    def black_bishop_has_right_moves(self, init_space: Space, expected_spaces: list[Space]):
        bishop = self.make_black_bishop(init_space)
        actual_spaces: list[Space] = []
        for m in bishop.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))
        
        assert len(actual_spaces) == len(expected_spaces)

        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]

    def test_black_bishop(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            init_space = Space('c', 8)
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space)
            self.black_bishop_has_right_moves(init_space, expected_spaces)