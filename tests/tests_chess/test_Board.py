from __future__ import annotations
import unittest
from dataclasses import dataclass
from typing import Dict
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

    def generate_pawn_opened_expected(self, pawn: Pawn, opened_space: Space) -> list[list[Space]]:
        expected: list[list[Space]] = []
        lesser_file = pawn.position.decrease_file()
        greater_file = pawn.position.increase_file()
        if pawn.color == WHITE:
            expected.append([
                Space(
                    opened_space.file,
                    opened_space.increase_rank()
                )
            ])
        else:
            expected.append([
                Space(
                    opened_space.file,
                    opened_space.decrease_rank()
                )
            ])
        if lesser_file is not None:
            expected.append([
                Space(
                    lesser_file,
                    expected[0][0].rank
                )
            ])
        if greater_file is not None:
            expected.append([
                Space(
                    greater_file,
                    expected[0][0].rank
                )
            ])
        expected = sorted(expected, key=lambda p: (p[0].file, p[0].rank))
        return expected

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
                    InputData(board, piece, piece.position),
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
                    InputData(board, piece, piece.position), 
                    expected_moves
                    )
                with self.subTest(f"expect {expected_moves[:-1]}", piece=piece):
                    self.confirm_moves(test_case)

    def test_white_pawn_opening(self):
        board = Board()
        available_moves: Dict[Piece, list[str]] = {}
        all_moves = board.offer_moves(WHITE)
        for k in all_moves:
            moves = all_moves[k]
            if len(moves) > 0 and "Pinned" not in moves:
                available_moves[k] = moves

        for piece in available_moves:
            if isinstance(piece, Pawn):
                for move in available_moves[piece]:
                    [file, rank] = list(move)
                    move_space = Space(file, int(rank))
                    expected: list[list[Space]] = self.generate_pawn_opened_expected(piece, move_space)
                    test_case: CaseData = CaseData(
                        InputData(board, piece, move_space),
                        expected
                    )
                    with self.subTest(f"{expected}", move=f"{piece} -> {move_space}"):
                        board.apply_move(piece, move_space)
                        self.confirm_moves(test_case)
                        assert piece.developed
    
    def test_black_pawn_opening(self):
        board = Board()
        available_moves: Dict[Piece, list[str]] = {}
        all_moves = board.offer_moves(BLACK)
        for k in all_moves:
            moves = all_moves[k]
            if len(moves) > 0 and "Pinned" not in moves:
                available_moves[k] = moves
        
        for piece in available_moves:
           if isinstance(piece, Pawn):
                for move in available_moves[piece]:
                    [file, rank] = list(move)
                    move_space = Space(file, int(rank))
                    expected: list[list[Space]] = self.generate_pawn_opened_expected(piece, move_space)
                    test_case: CaseData = CaseData(
                        InputData(board, piece, move_space),
                        expected
                    )
                    with self.subTest(f"{expected}", move=f"{piece} -> {move_space}"):
                        board.apply_move(piece, move_space)
                        self.confirm_moves(test_case)
                        assert piece.developed
    
    def generate_knight_opened_expected(self, knight: Knight, move: Space) -> list[list[Space]]:
        expected: list[list[Space]] = []
        new_rank = None
        if knight.color == WHITE:
            new_rank = knight.position.increase_rank()
        else:
            new_rank = knight.position.decrease_rank()
        lesser_file = knight.position.decrease_file()
        greater_file = knight.position.increase_file()
        expected.extend([
            [Space(lesser_file, new_rank)],
            [Space(greater_file, new_rank)]
        ])
        expected = sorted(expected, key=lambda p: (p[0].file, p[0].rank))
        return expected

    def test_white_knight_opening(self):
        board = Board()
        available_moves: Dict[Piece, list[str]] = {}
        all_moves = board.offer_moves(WHITE)
        for k in all_moves:
            moves = all_moves[k]
            if len(moves) > 0 and "Pinned" not in moves:
                available_moves[k] = moves
        
        for piece in available_moves:
           if isinstance(piece, Knight):
                for move in available_moves[piece]:
                    [file, rank] = list(move[1:])
                    move_space = Space(file, int(rank))
                    expected: list[list[Space]] = self.generate_knight_opened_expected(piece, move_space)
                    test_case: CaseData = CaseData(
                        InputData(board, piece, move_space),
                        expected
                    )
                    with self.subTest(f"{expected}", move=f"{piece} -> {move_space}"):
                        board.apply_move(piece, move_space)
                        self.confirm_moves(test_case)
                        assert piece.developed

    def test_black_knight_opening(self):
        board = Board()
        available_moves: Dict[Piece, list[str]] = {}
        all_moves = board.offer_moves(BLACK)
        for k in all_moves:
            moves = all_moves[k]
            if len(moves) > 0 and "Pinned" not in moves:
                available_moves[k] = moves
        
        for piece in available_moves:
           if isinstance(piece, Knight):
                for move in available_moves[piece]:
                    [file, rank] = list(move)
                    move_space = Space(file, int(rank))
                    expected: list[list[Space]] = self.generate_knight_opened_expected(piece, move_space)
                    test_case: CaseData = CaseData(
                        InputData(board, piece, move_space),
                        expected
                    )
                    with self.subTest(f"{expected}", move=f"{piece} -> {move_space}"):
                        board.apply_move(piece, move_space)
                        self.confirm_moves(test_case)
                        assert piece.developed

@dataclass
class CaseData:
    input: InputData
    expected: list[list[Space]]

@dataclass
class InputData:
    board: Board
    piece: Piece
    move: Space