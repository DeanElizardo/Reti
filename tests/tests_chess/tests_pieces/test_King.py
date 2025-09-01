from __future__ import annotations
from dataclasses import dataclass
import unittest
from src.chess.pieces.King import King
from src.chess.Kernel import *
from src.chess.Space import Space

class TestKing(unittest.TestCase):
    def king_factory(self, color: str, space: Space) -> King:
        return King(color, space)
    
    def make_white_king(self, space: Space) -> King:
        return self.king_factory(WHITE, space)
    
    def make_black_king(self, space: Space) -> King:
        return self.king_factory(BLACK, space)
    
    def generate_all_spaces(self) -> list[Space]:
        all_spaces: list[Space] = []
        for file in BOARD_FILES:
            for rank in BOARD_RANKS:
                all_spaces.append(Space(file, rank))
        return all_spaces
    
    def generate_expected_spaces(self, init_space: Space, add_castle: bool) -> list[Space]:
        expected_spaces: list[Space] = []
        if init_space.increase_file() is not None:
            s = Space(init_space.increase_file(), init_space.rank)
            expected_spaces.append(s)
        if init_space.decrease_file() is not None:
            s = Space(init_space.decrease_file(), init_space.rank)
            expected_spaces.append(s)
        if init_space.increase_rank() is not None:
            s = Space(init_space.file, init_space.increase_rank())
            expected_spaces.append(s)
        if init_space.decrease_rank() is not None:
            s = Space(init_space.file, init_space.decrease_rank())
            expected_spaces.append(s)
        if init_space.increase_file() is not None and init_space.increase_rank() is not None:
            s = Space(init_space.increase_file(), init_space.increase_rank())
            expected_spaces.append(s)
        if init_space.increase_file() is not None and init_space.decrease_rank() is not None:
            s = Space(init_space.increase_file(), init_space.decrease_rank())
            expected_spaces.append(s)
        if init_space.decrease_file() is not None and init_space.increase_rank() is not None:
            s = Space(init_space.decrease_file(), init_space.increase_rank())
            expected_spaces.append(s)
        if init_space.decrease_file() is not None and init_space.decrease_rank() is not None:
            s = Space(init_space.decrease_file(), init_space.decrease_rank())
            expected_spaces.append(s)
        if add_castle:
            expected_spaces.append(
                Space(init_space.decrease_file(1), init_space.rank)
            )
            expected_spaces.append(
                Space(init_space.increase_file(1), init_space.rank)
            )
            expected_spaces.append(
                Space(init_space.decrease_file(2), init_space.rank)
            )
            expected_spaces.append(
                Space(init_space.increase_file(2), init_space.rank)
            )
        expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))
        return expected_spaces
    
    def white_king_has_right_moves(self, case: CaseData):
        king = self.make_white_king(Space('e', 1))
        king.position = case.init_space
        king.developed = king.position != Space('e', 1)
        king.get_moves()
        actual_spaces: list[Space] = []
        for m in king.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces= sorted(actual_spaces, key=lambda p: (p.file, p.rank))

        assert len(actual_spaces) == len(case.expected_spaces)

        for idx in range(len(case.expected_spaces)):
            assert actual_spaces[idx] == case.expected_spaces[idx]

    def test_white_king(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space, init_space == Space('e', 1))
            expected_str = ""
            for s in expected_spaces:
                expected_str += f"{s} "
            test_case: CaseData = CaseData(init_space, expected_spaces)
            with self.subTest(f"expected {expected_str[:-1]}", init_space=init_space):
                self.white_king_has_right_moves(test_case)

    def black_king_has_right_moves(self, case: CaseData):
        king = self.make_black_king(Space('e', 8))
        king.position = case.init_space
        king.developed = king.position != Space('e', 8)
        king.get_moves()
        actual_spaces: list[Space] = []
        for m in king.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))
        
        assert len(actual_spaces) == len(case.expected_spaces)

        for idx in range(len(case.expected_spaces)):
            assert actual_spaces[idx] == case.expected_spaces[idx]

    def test_black_king(self):
        all_spaces = self.generate_all_spaces()
        for init_space in all_spaces:
            expected_spaces: list[Space] = self.generate_expected_spaces(init_space, init_space == Space('e', 8))
            expected_str = ""
            for s in expected_spaces:
                expected_str += f"{s} "
            test_case: CaseData = CaseData(init_space, expected_spaces)
            with self.subTest(f"expected {expected_str[:-1]}", init_space=init_space):
                self.black_king_has_right_moves(test_case)

@dataclass
class CaseData:
    init_space: Space
    expected_spaces: list[Space]