from __future__ import annotations
from dataclasses import dataclass
import unittest
from src.chess.pieces.Rook import Rook
from src.chess.Kernel import *
from src.chess.Space import Space

class TestRook(unittest.TestCase):
    def rook_factory(self, color: str, space: Space) -> Rook:
        return Rook(color, space)
    
    def make_white_rook(self, space: Space) -> Rook:
        return self.rook_factory(WHITE, space)
    
    def make_black_rook(self, space: Space) -> Rook:
        return self.rook_factory(BLACK, space)
    
    def generate_all_spaces(self) -> list[Space]:
        all_spaces: list[Space] = []
        for file in BOARD_FILES:
            for rank in BOARD_RANKS:
                all_spaces.append(Space(file, rank))
        return all_spaces
    
    def generate_expected_spaces(self, init_space: Space) -> list[Space]:
        expected_spaces: list[Space] = []
        s = Space(init_space.file, init_space.rank)
        while s.increase_file() is not None:
            s = Space(s.increase_file(), init_space.rank)
            expected_spaces.append(s)
        s = Space(init_space.file, init_space.rank)
        while s.decrease_file() is not None:
            s = Space(s.decrease_file(), init_space.rank)
            expected_spaces.append(s)
        s = Space(init_space.file, init_space.rank)
        while s.increase_rank() is not None:
            s = Space(init_space.file, s.increase_rank())
            expected_spaces.append(s)
        s = Space(init_space.file, init_space.rank)
        while s.decrease_rank() is not None:
            s = Space(init_space.file, s.decrease_rank())
            expected_spaces.append(s)
        expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))
        return expected_spaces
    
    def white_rook_has_right_moves(self, case: CaseData):
        rook = self.make_white_rook(case.init_space)
        actual_spaces: list[Space] = []
        for m in rook.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces= sorted(actual_spaces, key=lambda p: (p.file, p.rank))

        assert len(actual_spaces) == len(case.expected_spaces)

        for idx in range(len(case.expected_spaces)):
            assert actual_spaces[idx] == case.expected_spaces[idx]

    def test_white_rook(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space)
            expected_str = ""
            for s in expected_spaces:
                expected_str += f"{s} "
            test_case: CaseData = CaseData(init_space, expected_spaces)
            with self.subTest(f"expected {expected_str[:-1]}", init_space=init_space):
                self.white_rook_has_right_moves(test_case)

    def black_rook_has_right_moves(self, case: CaseData):
        rook = self.make_black_rook(case.init_space)
        actual_spaces: list[Space] = []
        for m in rook.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))
        
        assert len(actual_spaces) == len(case.expected_spaces)

        for idx in range(len(case.expected_spaces)):
            assert actual_spaces[idx] == case.expected_spaces[idx]

    def test_black_rook(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space)
            expected_str = ""
            for s in expected_spaces:
                expected_str += f"{s} "
            test_case: CaseData = CaseData(init_space, expected_spaces)
            with self.subTest(f"expected {expected_str[:-1]}", init_space=init_space):
                self.black_rook_has_right_moves(test_case)

@dataclass
class CaseData:
    init_space: Space
    expected_spaces: list[Space]