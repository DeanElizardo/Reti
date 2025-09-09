from typing import Dict
from src.chess.Kernel import *
from src.chess.Board import Board
from src.chess.Space import Space
from src.chess.pieces.Piece import Piece

class Game:
    def __init__(self):
        self.board = Board()
        self.player_turn = WHITE

    def display_moves(self, moves: Dict[Piece, list[str]]) -> None:
        for piece in moves:
            if len(moves[piece]) > 0:
                marker = piece.get_marker()
                print(f"{marker}:")
                for move in moves[piece]:
                    print(f" * {move}")
    
    def get_player_move(self, moves: Dict[Piece, list[str]]) -> tuple[Piece, Space]:
        player_choice: str = ""
        while not any(player_choice in choices for choices in moves.values()):
            player_choice: str = input("MOVE: ")
        selected_piece: Piece = [p for p in moves if player_choice in moves[p]][0]
        [file_coord, rank_coord] = list(player_choice[len(player_choice) % 2:])
        space = Space(file_coord, int(rank_coord))
        return (selected_piece, space)

    def turn(self):
        print(f"=== {self.player_turn} to play ===")
        self.board.validate_moves(self.player_turn)
        # Offer a list of moves for this player by piece
        moves = self.board.offer_moves(self.player_turn)
        self.display_moves(moves)
        # Read and validate player choice
        (selected_piece, new_space) = self.get_player_move(moves)
        # Update piece positions
        self.board.apply_move(selected_piece, new_space)
        # Update player turn
        self.player_turn = [player_color for player_color in [WHITE, BLACK] if player_color != self.player_turn][0]

    def play(self):
        while not self.board.detect_checkmate(self.player_turn):
            self.turn()