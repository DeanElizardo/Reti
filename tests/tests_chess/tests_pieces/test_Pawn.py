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
    
    def generate_expected_spaces(self, init_space: Space, color: str, developing_move: bool) -> list[Space]:
        expected_spaces: list[Space] = []
        if color == WHITE:
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
            if developing_move:
                try:
                    s = Space(init_space.file, init_space.increase_rank(2))
                    expected_spaces.append(s)
                except: pass
            expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))
        else:
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
            if developing_move:
                try:
                    s = Space(init_space.file, init_space.decrease_rank(2))
                    expected_spaces.append(s)
                except: pass
            expected_spaces = sorted(expected_spaces, key=lambda p: (p.file, p.rank))
        return expected_spaces
    
    def white_pawn_has_right_moves_on_init(self, init_space: Space, expected_spaces: list[Space]):
        pawn = self.make_white_pawn(init_space)
        actual_spaces: list[Space] = []
        for m in pawn.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))
        
        assert len(actual_spaces) == len(expected_spaces)
        
        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]
        
    def black_pawn_has_right_moves_on_init(self, init_space: Space, expected_spaces: list[Space]):
        pawn = self.make_black_pawn(init_space)
        actual_spaces: list[Space] = []
        for m in pawn.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))
        
        assert len(actual_spaces) == len(expected_spaces)

        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]

    def black_pawn_moves_update_correctly(self, pawn: Pawn, expected_spaces: list[Space]):
        actual_spaces: list[Space] = []
        for m in pawn.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))

        assert len(actual_spaces) == len(expected_spaces)

        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]

    def white_pawn_moves_update_correctly(self, pawn: Pawn, expected_spaces: list[Space]):
        actual_spaces: list[Space] = []
        for m in pawn.moves:
            for s in m:
                actual_spaces.append(s)
        actual_spaces = sorted(actual_spaces, key=lambda p: (p.file, p.rank))

        assert len(actual_spaces) == len(expected_spaces)

        for idx in range(len(expected_spaces)):
            assert actual_spaces[idx] == expected_spaces[idx]

###############################################################################
### BLACK PAWN TESTS ##########################################################
###############################################################################

    def test_black_init_a7(self):
        init_space = Space('a', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_black_init_b7(self):
        init_space = Space('b', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_black_init_c7(self):
        init_space = Space('c', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_black_init_d7(self):
        init_space = Space('d', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_black_init_e7(self):
        init_space = Space('e', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_black_init_f7(self):
        init_space = Space('f', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_black_init_g7(self):
        init_space = Space('g', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_black_init_h7(self):
        init_space = Space('h', 7)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, BLACK, True)
        self.black_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def black_develop_from(self, space: Space):
        pawn: Pawn = self.make_black_pawn(space)
        for m in pawn.moves:
            for s in m:
                pawn.move(s)
                expected_moves: list[Space] = self.generate_expected_spaces(s, BLACK, False)
                self.black_pawn_moves_update_correctly(pawn, expected_moves)
                pawn.move(space)
                pawn.developed = False

    def test_black_develop_from_a7(self):
        self.black_develop_from(Space('a', 7))

    def test_black_develop_from_b7(self):
        self.black_develop_from(Space('b', 7))

    def test_black_develop_from_c7(self):
        self.black_develop_from(Space('c', 7))

    def test_black_develop_from_d7(self):
        self.black_develop_from(Space('d', 7))

    def test_black_develop_from_e7(self):
        self.black_develop_from(Space('e', 7))

    def test_black_develop_from_f7(self):
        self.black_develop_from(Space('f', 7))

    def test_black_develop_from_g7(self):
        self.black_develop_from(Space('g', 7))

    def test_black_develop_from_h7(self):
        self.black_develop_from(Space('h', 7))

    def black_move_twice(self, init: Space, first_move: Space):
        pawn: Pawn = self.make_black_pawn(init)
        pawn.move(first_move)
        pawn.move(pawn.moves[0][0])
        expected: list[Space] = self.generate_expected_spaces(pawn.position, BLACK, False)
        self.black_pawn_moves_update_correctly(pawn, expected)

    def test_black_move_twice_a7(self):
        init: Space = Space('a', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

    def test_black_move_twice_b7(self):
        init: Space = Space('b', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

    def test_black_move_twice_c7(self):
        init: Space = Space('c', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

    def test_black_move_twice_d7(self):
        init: Space = Space('d', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

    def test_black_move_twice_e7(self):
        init: Space = Space('e', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

    def test_black_move_twice_f7(self):
        init: Space = Space('f', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

    def test_black_move_twice_g7(self):
        init: Space = Space('h', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

    def test_black_move_twice_h7(self):
        init: Space = Space('h', 7)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.black_move_twice(init, space)

###############################################################################
### WHITE PAWN TESTS ##########################################################
###############################################################################

    def test_white_init_a2(self):
        init_space = Space('a', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_white_init_b2(self):
        init_space = Space('b', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)
    
    def test_white_init_c2(self):
        init_space = Space('c', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_white_init_d2(self):
        init_space = Space('d', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_white_init_e2(self):
        init_space = Space('e', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_white_init_f2(self):
        init_space = Space('f', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_white_init_g2(self):
        init_space = Space('g', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def test_white_init_h2(self):
        init_space = Space('h', 2)
        expected_spaces: list[Space] = self.generate_expected_spaces(init_space, WHITE, True)
        self.white_pawn_has_right_moves_on_init(init_space, expected_spaces)

    def white_develop_from(self, space: Space):
        pawn: Pawn = self.make_white_pawn(space)
        for m in pawn.moves:
            for s in m:
                pawn.move(s)
                expected_moves: list[Space] = self.generate_expected_spaces(s, WHITE, False)
                self.white_pawn_moves_update_correctly(pawn, expected_moves)
                pawn.move(space)
                pawn.developed = False

    def test_white_develop_from__a2(self):
        self.white_develop_from(Space('a', 2))

    def test_white_develop_from_b2(self):
        self.white_develop_from(Space('b', 2))

    def test_white_develop_from_c2(self):
        self.white_develop_from(Space('c', 2))

    def test_white_develop_from_d2(self):
        self.white_develop_from(Space('d', 2))

    def test_white_develop_from_e2(self):
        self.white_develop_from(Space('d', 2))

    def test_white_develop_from_f2(self):
        self.white_develop_from(Space('e', 2))

    def test_white_develop_from_g2(self):
        self.white_develop_from(Space('f', 2))

    def test_white_develop_from_h2(self):
        self.white_develop_from(Space('h', 2))

    def white_move_twice(self, init: Space, first_move: Space):
        pawn: Pawn = self.make_white_pawn(init)
        pawn.move(first_move)
        pawn.move(pawn.moves[0][0])
        expected: list[Space] = self.generate_expected_spaces(pawn.position, WHITE, False)
        self.white_pawn_moves_update_correctly(pawn, expected)

    def test_white_move_twice_a2(self):
        init: Space = Space('a', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)

    def test_white_move_twice_b2(self):
        init: Space = Space('b', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)

    def test_white_move_twice_c2(self):
        init: Space = Space('c', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)

    def test_white_move_twice_d2(self):
        init: Space = Space('d', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)

    def test_white_move_twice_e2(self):
        init: Space = Space('e', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)

    def test_white_move_twice_f2(self):
        init: Space = Space('f', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)

    def test_white_move_twice_g2(self):
        init: Space = Space('h', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)

    def test_white_move_twice_h2(self):
        init: Space = Space('h', 2)
        pawn: Pawn = self.make_black_pawn(init)
        for moves in pawn.moves:
            for space in moves:
                self.white_move_twice(init, space)