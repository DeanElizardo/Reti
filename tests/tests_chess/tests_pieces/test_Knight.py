from __future__ import annotations
import unittest
from dataclasses import dataclass
from src.chess.pieces.Knight import Knight
from src.chess.Kernel import *
from src.chess.Space import Space

class TestKnight(unittest.TestCase):
    def knight_factory(self, color: str, space: Space) -> Knight:
        return Knight(color, space)
    
    def make_white_knight(self, space: Space) -> Knight:
        return self.knight_factory(WHITE, space)
    
    def make_black_knight(self, space: Space) -> Knight:
        return self.knight_factory(WHITE, space)
    
    def generate_all_spaces(self) -> list[Space]:
        all_spaces: list[Space] = []
        for file in BOARD_FILES:
            for rank in BOARD_RANKS:
                all_spaces.append(Space(file, rank))
        return all_spaces
    
    def generate_expected_spaces(self, init_space: Space) -> list[Space]:
        expected_spaces: list[Space] = []
        rank_2s: list[int] = [
            r for r in [
                init_space.increase_rank(2),
                init_space.decrease_rank(2)
            ]
            if r is not None
        ]
        file_2s: list[str] = [
            f for f in [
                init_space.increase_file(2),
                init_space.decrease_file(2)
            ]
            if f is not None
        ]
        rank_1s: list[int] = [
            r for r in [
                init_space.increase_rank(1),
                init_space.decrease_rank(1)
            ]
            if r is not None
        ]
        file_1s: list[str] = [
            f for f in [
                init_space.increase_file(1),
                init_space.decrease_file(1)
            ]
            if f is not None
        ]
        for r in rank_2s:
            for f in file_1s:
                expected_spaces.append(Space(f, r))
        for f in file_2s:
            for r in rank_1s:
                expected_spaces.append(Space(f, r))
        expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))
        return expected_spaces
    
    def piece_has_right_moves(self, piece: Knight, expected_spaces: list[Space]):
        actual_spaces: list[Space] = []
        for m in piece.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key= lambda p: (p.file, p.rank))

        assert len(actual_spaces) == len(expected_spaces)

        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]
    
    def white_knight_has_right_moves(self, case: CaseData):
        knight = self.make_white_knight(case.init_space)
        self.piece_has_right_moves(knight, case.expected_spaces)

    def black_knight_has_right_moves(self, case: CaseData):
        knight = self.make_black_knight(case.init_space)
        self.piece_has_right_moves(knight, case.expected_spaces)

    def test_white_knight_cases(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space)
            test_case: CaseData = CaseData(init_space, expected_spaces)
            expected_str: str = ""
            for s in expected_spaces:
                expected_str += f"{s} "
            with self.subTest(f"expect {expected_str[:-1]}", init_space=init_space):
                self.white_knight_has_right_moves(test_case)

    def test_black_knight(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space)
            test_case: CaseData = CaseData(init_space, expected_spaces)
            expected_str: str = ""
            for s in expected_spaces:
                expected_str += f"{s} "
            with self.subTest(f"expect {expected_str[:-1]}", init_space=init_space):
                self.black_knight_has_right_moves(test_case)

@dataclass
class CaseData:
    init_space: Space
    expected_spaces: list[Space]
