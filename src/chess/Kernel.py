class PieceDescriptor:
    def __init__(self, name: str, symbol: str, points: int):
        self.NAME: str = name
        self.SYMB: str = symbol
        self.POINTS: int = points

BOARD_RANKS: list[int] = [ 1, 2, 3, 4, 5, 6, 7, 8 ]
BOARD_FILES: list[str] = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
WHITE: str = "white"
BLACK: str = "black"
KING: PieceDescriptor = PieceDescriptor('King', 'K', 0)
QUEEN: PieceDescriptor = PieceDescriptor('Queen', 'Q', 9)
ROOK: PieceDescriptor = PieceDescriptor('Rook', 'R', 5)
BISHOP: PieceDescriptor = PieceDescriptor('Bishop', 'B', 3)
KNIGHT: PieceDescriptor = PieceDescriptor('Knight', 'N', 3)
PAWN: PieceDescriptor = PieceDescriptor('Pawn', '', 1)