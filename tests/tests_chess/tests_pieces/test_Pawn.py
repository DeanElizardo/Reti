import unittest
from src.chess.pieces.Pawn import Pawn
from src.chess.Kernel import *
from src.chess.Space import Space

class TestPawn(unittest.TestCase):
    def pawn_factory(self, color: str, space: Space) -> Pawn:
        return Pawn(color, space)
    
    def make_white_pawn(self, space: Space) -> Pawn:
        return self.pawn_factory(WHITE, space)
    
    def make_black_pawn(self, space: Space) -> Pawn:
        return self.pawn_factory(BLACK, space)
    
    def test_white_pawn_has_right_moves_on_init(self):
        
        init_space = Space('a', 2)
        expected_spaces: list[Space] = []
        try:
            s = Space(init_space.file, init_space.increase_rank())
            expected_spaces.append(s)
        except: pass
        try:
            s = Space(init_space.increase_file(), init_space.increase_rank())
            expected_spaces.append(s)
        except: pass
        try:
            s = Space(init_space.decrease_file(), init_space.increase_rank())
            expected_spaces.append(s)
        except: pass
        try:
            s = Space(init_space.file, init_space.increase_rank(2))
            expected_spaces.append(s)
        except: pass
        expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))
        
        
        pawn = self.make_white_pawn(init_space)
        actual_spaces: list[Space] = []
        for m in pawn.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))
        
        assert len(actual_spaces) == len(expected_spaces)
        
        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]
        
    def test_black_pawn_has_right_moves_on_init(self):
        init_space = Space('a', 7)
        expected_spaces: list[Space] = []
        try:
            s = Space(init_space.file, init_space.decrease_rank())
            expected_spaces.append(s)
        except: pass
        try:
            s = Space(init_space.increase_file(), init_space.decrease_rank())
            expected_spaces.append(s)
        except: pass
        try:
            s = Space(init_space.decrease_file(), init_space.decrease_rank())
            expected_spaces.append(s)
        except: pass
        try:
            s = Space(init_space.file, init_space.decrease_rank(2))
            expected_spaces.append(s)
        except: pass
        expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))

        pawn = self.make_black_pawn(init_space)
        actual_spaces: list[Space] = []
        for m in pawn.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))
        
        assert len(actual_spaces) == len(expected_spaces)

        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]
            
    def test_white_pawn_updates_after_move(self):
        initial_space = Space('b', 2)