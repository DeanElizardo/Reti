from __future__ import annotations
import unittest
from dataclasses import dataclass
# from typing import Union, Dict
from src.chess.Kernel import *
from src.chess.Board import Board
from src.chess.Space import Space
# from src.chess.Materiel import Materiel
from src.chess.pieces.Piece import Piece
from src.chess.pieces.Pawn import Pawn
# from src.chess.pieces.Rook import Rook
from src.chess.pieces.Knight import Knight
# from src.chess.pieces.Bishop import Bishop
# from src.chess.pieces.Queen import Queen
# from src.chess.pieces.King import King

class TestBoard(unittest.TestCase):
    def generate_pawn_openings(self, pawn: Pawn) -> list[list[Space]]:
        init_space: Space = pawn.position.clone()
        openings: list[list[Space]] = []
        if pawn.color == WHITE:
            openings.extend([
                [
                    Space(init_space.file, init_space.increase_rank(1))
                ],
                [
                    Space(init_space.file, init_space.increase_rank(2))
                ]
            ])
        else:
            openings.extend([
                [
                    Space(init_space.file, init_space.decrease_rank(1))
                ],
                [
                    Space(init_space.file, init_space.decrease_rank(2))
                ]
            ])
        openings = sorted(openings, key=lambda p: (p[0].file, p[0].rank))
        return openings
    
    def generate_knight_openings(self, knight: Knight) -> list[list[Space]]:
        init_space: Space = knight.position.clone()
        openings: list[list[Space]] = []
        if knight.color == WHITE:
            openings.extend([
                [
                    Space(init_space.increase_file(1), init_space.increase_rank(2))
                ],
                [
                    Space(init_space.decrease_file(1), init_space.increase_rank(2))
                ]
            ])
        else:
            openings.extend([
                [
                    Space(init_space.increase_file(1), init_space.decrease_rank(2))
                ],
                [
                    Space(init_space.decrease_file(1), init_space.decrease_rank(2))
                ]
            ])
        openings = sorted(openings, key=lambda p: (p[0].file, p[0].rank))
        return openings

    def confirm_moves(self, case: CaseData):
        board = case.input.board
        piece = case.input.piece
        expect = case.expected
        piece_position: Space = piece.position
        assert board.spaces[piece_position] == piece
        actual_positions: list[list[Space]] = sorted([m for m in piece.moves if len(m) > 0], key=lambda p: (p[0].file, p[0].rank))
        assert len(actual_positions) == len(expect)
        for idx in range(len(expect)):
            expected_lane: list[Space] = expect[idx]
            actual_lane: list[Space] = actual_positions[idx]
            self.assertCountEqual(expected_lane, actual_lane)

    def test_init_white_pieces_correct_moves(self):
        board = Board()
        for piece_collection in board.materiel[WHITE]:
            for piece in piece_collection:
                expected_moves: list[list[Space]] = []
                expect_str = ""
                if isinstance(piece, Pawn): expected_moves = self.generate_pawn_openings(piece)
                if isinstance(piece, Knight): expected_moves = self.generate_knight_openings(piece)
                for s in expected_moves:
                    expect_str += f"{s} "
                test_case: CaseData = CaseData(
                    InputData(board, piece),
                    expected_moves
                    )
                with self.subTest(f"expect {expected_moves[:-1]}", piece=piece):
                    self.confirm_moves(test_case)

    def test_init_black_pieces_correct_moves(self):
        board = Board()
        for piece_collection in board.materiel[BLACK]:
            for piece in piece_collection:
                expected_moves: list[list[Space]] = []
                expect_str = ""
                if isinstance(piece, Pawn): expected_moves = self.generate_pawn_openings(piece)
                if isinstance(piece, Knight): expected_moves = self.generate_knight_openings(piece)
                for s in expected_moves:
                    expect_str += f"{s} "
                test_case: CaseData = CaseData(
                    InputData(board, piece), 
                    expected_moves
                    )
                with self.subTest(f"expect {expected_moves[:-1]}", piece=piece):
                    self.confirm_moves(test_case)

    def test_white_pawn_opening(self):
        # TODO: Write tests that deal with pawn openings for black and white
        pass

@dataclass
class CaseData:
    input: InputData
    expected: list[list[Space]]

@dataclass
class InputData:
    board: Board
    piece: Piece