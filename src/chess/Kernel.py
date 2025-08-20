class PieceIdentifier:
    def __init__(self, name: str, symbol: str):
        self.NAME: str = name
        self.SYMB: str = symbol

BOARD_RANKS: list[int] = [ 1, 2, 3, 4, 5, 6, 7, 8 ]
BOARD_FILES: list[str] = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
WHITE: str = "white"
BLACK: str = "black"
KING: PieceIdentifier = PieceIdentifier('King', 'K')
QUEEN: PieceIdentifier = PieceIdentifier('Queen', 'Q')
ROOK: PieceIdentifier = PieceIdentifier('Rook', 'R')
KNIGHT: PieceIdentifier = PieceIdentifier('Knight', 'N')
BISHOP: PieceIdentifier = PieceIdentifier('Bishop', 'B')
PAWN: PieceIdentifier = PieceIdentifier('Pawn', '')