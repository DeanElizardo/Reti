from __future__ import annotations
from typing import Union, Dict
from src.chess.Kernel import *
from src.chess.Space import Space
from src.chess.Materiel import Materiel
from src.chess.pieces.Piece import Piece
from src.chess.pieces.Pawn import Pawn
from src.chess.pieces.Rook import Rook
from src.chess.pieces.Knight import Knight
from src.chess.pieces.Bishop import Bishop
from src.chess.pieces.Queen import Queen
from src.chess.pieces.King import King

class Board:
    def __init__(self):
        self.materiel = self.generate_pieces()
        self.spaces: Dict[Space, Union[Piece, None]] = {}
        self.attacks: Dict[str, Dict[Piece, list[Space]]] = {
            WHITE: {},
            BLACK: {}
        }
        self.valid_moves: list[Space] = []
        for file in BOARD_FILES:
            for rank in BOARD_RANKS:
                space = Space(file, rank)
                self.spaces[space] = None
        self.captures: Dict[str, list[Piece]] = {
            BLACK: [],
            WHITE: []
        }
        self.setup_board()
        self.material_advantage_to: str = "neither"

    def generate_pieces(self) -> Dict[str, Materiel]:
        return {
            BLACK: Materiel(BLACK),
            WHITE: Materiel(WHITE)
        }
    
    def set_space(self, piece: Piece):
        self.spaces[piece.position] = piece

    def setup_board(self):
        for materiel_color in self.materiel:
            materiel_collection = self.materiel[materiel_color]
            for king in materiel_collection.king:
                self.set_space(king)
                self.attacks[materiel_color][king] = []
            for queen in materiel_collection.queens:
                self.set_space(queen)
                self.attacks[materiel_color][queen] = []
            for rook in materiel_collection.rooks:
                self.set_space(rook)
                self.attacks[materiel_color][rook] = []
            for knight in materiel_collection.knights:
                self.set_space(knight)
                self.attacks[materiel_color][knight] = []
            for bishop in materiel_collection.bishops:
                self.set_space(bishop)
                self.attacks[materiel_color][bishop] = []
            for pawn in materiel_collection.pawns:
                self.set_space(pawn)
                self.attacks[materiel_color][pawn] = []
            self.validate_moves(materiel_color)

    def validate_moves(self, color: str) -> None:
        enemy_color: str = [c for c in [WHITE, BLACK] if c != color][0]
        self.valid_moves.clear()
        for attacking_piece in self.attacks[color]:
            self.attacks[color][attacking_piece].clear()

        # Get all of the moves that would pin an opposing piece
        # and the extent of all possible paths
        piece_inventory: Materiel = self.materiel[color]
        for pieces in piece_inventory:
            for piece in pieces:
                for attack_line_idx in range(len(piece.moves)):
                    attack_line = piece.moves[attack_line_idx]
                    new_moves: list[Space] = []
                    # piece is a pawn
                    if isinstance(piece, Pawn):
                        for space_idx in range(len(attack_line)):
                            space = attack_line[space_idx]
                            occupant = self.spaces[space]
                            if occupant is not None:
                                if space.file == piece.position.file:
                                    break
                                else:
                                    if occupant.color != piece.color:
                                        new_moves.append(space)
                            else:
                                if space.file == piece.position.file:
                                    new_moves.append(space)
                        if piece.passant_armed:
                            passant_capture_rank: Union[int, None] = None
                            if piece.color == WHITE:
                                passant_capture_rank = piece.position.increase_rank()
                            else:
                                passant_capture_rank = piece.position.decrease_rank()
                            if passant_capture_rank is not None:
                                lesser_file: Union[str, None] = piece.position.decrease_file()
                                greater_file: Union[str, None] = piece.position.increase_file()
                                if lesser_file is not None:
                                    lesser_neighbor: Union[Piece, None] = self.spaces[Space(lesser_file, piece.position.rank)]
                                    lesser_passant_capture = Space(lesser_file, passant_capture_rank)
                                    lpc_occupant: Union[Piece, None] = self.spaces[lesser_passant_capture]
                                    if isinstance(lesser_neighbor, Pawn) and lpc_occupant is None and lesser_neighbor.passant_vuln:
                                        new_moves.append(lesser_passant_capture)
                                if greater_file is not None:
                                    greater_neighbor: Union[Piece, None] = self.spaces[Space(greater_file, piece.position.rank)]
                                    greater_passant_capture = Space(greater_file, passant_capture_rank)
                                    gpc_occupant: Union[Piece, None] = self.spaces[greater_passant_capture]
                                    if isinstance(greater_neighbor, Pawn) and gpc_occupant is None and greater_neighbor.passant_vuln:
                                        new_moves.append(greater_passant_capture)
                    # piece is not a pawn                                    
                    else:
                        for space_idx in range(len(attack_line)):
                            space = attack_line[space_idx]
                            occupant = self.spaces[space]
                            if isinstance(occupant, Piece):
                                if occupant.color == piece.color:
                                    # struck an allied piece
                                    break
                                else:
                                    # struck an enemy piece
                                    self.attacks[color][piece].append(space)
                                    new_moves.append(space)
                                    if isinstance(occupant, King):
                                        occupant.in_check = True
                                        piece.check()
                                    else:
                                        for next_space in attack_line[space_idx:]:
                                            next_occupant = self.spaces[next_space]
                                            if next_occupant is not None:
                                                if next_occupant.color != piece.color and isinstance(next_occupant, King):
                                                    next_occupant.pin()
                                                    piece.check()
                                                    break
                                    break
                            else:
                                # struck an empty space
                                self.attacks[color][piece].append(space)
                                new_moves.append(space)
                    piece.moves[attack_line_idx] = new_moves
        # If the allied king is in check, filter
        # valid moves to those that would remove the check
        if self.materiel[color].king[0].in_check:
            # Where can the king move
            allowed_moves: list[Space] = []
            king_moves: list[Space] = []
            for move_list in self.materiel[color].king[0].moves:
                king_moves += move_list
            for enemy_piece in self.attacks[enemy_color]:
                enemy_attacks: list[Space] = self.attacks[enemy_color][enemy_piece]
                allowed_moves = [m for m in king_moves if m not in enemy_attacks and m not in allowed_moves]
            self.materiel[color].king[0].moves = [[m] for m in allowed_moves]

            # Only consider unpinned pieces
            movable_pieces = [piece for piece in self.attacks[color] if not piece.pinned and not isinstance(piece, King)]

            # What pieces can intercept a check
            checking_enemy_pieces = [enemy_piece for enemy_piece in self.attacks[enemy_color] if enemy_piece.checking]
            if len(checking_enemy_pieces) < 2:
                for piece in movable_pieces:
                    for enemy_piece in checking_enemy_pieces:
                        for defending_move_line_idx in range(len(piece.moves)):
                            defending_move_line = piece.moves[defending_move_line_idx]
                            for defending_space in defending_move_line:
                                for attacking_move_line in enemy_piece.moves:
                                    if defending_space in attacking_move_line:
                                        piece.moves[defending_move_line_idx] = [defending_space]
            else:
                for pieces in self.materiel[color]:
                    for piece in pieces:
                        if not isinstance(piece, King):
                            piece.moves = []

    def offer_moves(self, color: str) -> Dict[Piece, list[str]]:
        moves: Dict[Piece, list[str]] = {}
        for pieces in self.materiel[color]:
            for piece in pieces:
                moves[piece] = []
                if piece.pinned:
                    moves[piece].append("Pinned")
                    break
                for spaces in piece.moves:
                    for space in spaces:
                        move = f"{piece.symbol}{space.file}{space.rank}"
                        if move not in moves[piece]:
                            moves[piece].append(move)
        return moves
    
    def detect_checkmate(self, color: str) -> bool:
        checkmate: bool = self.materiel[color].king[0].in_check
        if not checkmate:
            return False
        for pieces in self.materiel[color]:
            for piece in pieces:
                for moves in piece.moves:
                    checkmate &= len(moves) == 0
        return checkmate
    
    def calculate_advantage(self) -> None:
        white_total = 0
        black_total = 0
        for pieces in self.materiel[WHITE]:
            for piece in pieces:
                white_total += piece.points
        for pieces in self.materiel[BLACK]:
            for piece in pieces:
                black_total += piece.points
        if white_total > black_total:
            self.material_advantage_to = WHITE
        elif black_total > white_total:
            self.material_advantage_to = BLACK
        else:
            self.material_advantage_to = "neither"
            
    def handle_capture(self, space: Space, attacking_color: str, captured_color: str) -> None:
        captured_piece: Union[Piece, None] = self.spaces[space]
        if captured_piece is None:
            return
        self.captures[attacking_color].append(captured_piece)
        if isinstance(captured_piece, Queen):
            self.materiel[attacking_color].queens.remove(captured_piece)
        elif isinstance(captured_piece, Rook):
            self.materiel[attacking_color].rooks.remove(captured_piece)
        elif isinstance(captured_piece, Bishop):
            self.materiel[attacking_color].bishops.remove(captured_piece)
        elif isinstance(captured_piece, Knight):
            self.materiel[attacking_color].knights.remove(captured_piece)
        elif isinstance(captured_piece, Pawn):
            self.materiel[attacking_color].pawns.remove(captured_piece)
        else:
            raise Exception("King capture is not allowed")
    
    def apply_move(self, piece: Piece, space: Space) -> None:
        del self.attacks[piece.color][piece]
        old_space = piece.position.clone()
        self.spaces[old_space] = None
        self.handle_capture(
            space,
            piece.color,
            [c for c in [BLACK, WHITE] if c != piece.color][0]
        )
        piece.move(space)
        self.calculate_advantage()
        self.spaces[space] = piece
        self.attacks[piece.color][piece] = []
    
    def promote_piece(self, piece: Piece):
        raise Exception("this method has not been implemented")