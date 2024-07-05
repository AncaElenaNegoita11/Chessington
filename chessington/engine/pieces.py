from __future__ import annotations
from abc import ABC, abstractmethod
from chessington.engine.data import Player, Square
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from chessington.engine.board import Board

class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player: Player):
        self.player = player

    @abstractmethod
    def get_available_moves(self, board: Board) -> List[Square]:
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """
    WHITE_PAWN_LINE = 1
    BLACK_PAWN_LINE = 6
    FORWARD_TWO_SPACES = 2
    LEFT = -1
    RIGHT = 1

    def get_moves_by_player_color(self):
        move_forward = 1 if self.player == Player.WHITE else -1
        row_first_time_move = self.WHITE_PAWN_LINE if self.player == Player.WHITE else self.BLACK_PAWN_LINE
        return move_forward, row_first_time_move

    def in_bounds(self, move) -> bool:
        return move in range(0, 8)

    def first_time_move(self, current_square, row_first_time_move, move_forward, board, list_moves):
        # Verify if it is the first time the pawn moves
        if current_square.row == row_first_time_move:
            square_two_spaces_in_front = Square.at(current_square.row + move_forward * self.FORWARD_TWO_SPACES,
                                                   current_square.col)
            # Can move two squares forward
            if self.in_bounds(square_two_spaces_in_front.row) and not board.get_piece(square_two_spaces_in_front):
                list_moves.append(square_two_spaces_in_front)

    def verify_attack_different_color(self, piece):
        return self.player != piece.player

    def verify_attack_diagonally(self, current_square, move_forward, board, list_moves):
        # Attack diagonally (2 spaces possible)
        square_diagonal_left = Square.at(current_square.row + move_forward, current_square.col + self.LEFT)
        square_diagonal_right = Square.at(current_square.row + move_forward, current_square.col + self.RIGHT)

        # Can't attack same color and if a piece isn't there
        if self.in_bounds(square_diagonal_left.col):
            diagonal_piece_left = board.get_piece(square_diagonal_left)
            if diagonal_piece_left and self.verify_attack_different_color(diagonal_piece_left):
                list_moves.append(square_diagonal_left)

        if self.in_bounds(square_diagonal_right.col):
            diagonal_piece_right = board.get_piece(square_diagonal_right)
            if diagonal_piece_right and self.verify_attack_different_color(diagonal_piece_right):
                list_moves.append(square_diagonal_right)

    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        list_moves = []
        move_forward, row_first_time_move = self.get_moves_by_player_color()

        square_in_front = Square.at(current_square.row + move_forward, current_square.col)
        # Can move forward at least once
        if self.in_bounds(square_in_front.row):
            if not board.get_piece(square_in_front):
                list_moves.append(square_in_front)
                # Verify first time move of pawn
                self.first_time_move(current_square, row_first_time_move, move_forward, board, list_moves)
            # Verify attack diagonally
            self.verify_attack_diagonally(current_square, move_forward, board, list_moves)

        return list_moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []


class MoveByDirection:
    FIRST_STEP = 1

    @staticmethod
    def in_bounds(move) -> bool:
        return move.row in range(0, 8) and move.col in range(0, 8)

    @staticmethod
    def get_position(current_square, current_piece, board, list_moves, step, direction):
        next_square = Square.at(current_square.row + direction.row * step,
                                current_square.col + direction.col * step)
        if MoveByDirection.in_bounds(next_square):
            piece = board.get_piece(next_square)
            if not piece:
                list_moves.append(next_square)
            else:
                if piece.player != current_piece.player:
                    list_moves.append(next_square)
                return 0
        else:
            return 0
        return 1

    @staticmethod
    def get_moves(current_piece, board, directions, not_king):
        current_square = board.find_piece(current_piece)
        list_moves = []
        for direction in directions:
            continue_moves = MoveByDirection.get_position(current_square, current_piece, board, list_moves,
                                                          MoveByDirection.FIRST_STEP, direction)
            if not_king and continue_moves:
                step = 2
                while True:
                    continue_moves = MoveByDirection.get_position(current_square, current_piece, board,
                                                                  list_moves, step, direction)
                    if not continue_moves:
                        break
                    step += 1

        return list_moves


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """
    directions = [Square(1, 1), Square(-1, 1), Square(-1, -1), Square(1, -1)]
    NOT_KING = 1

    def get_available_moves(self, board):
        return MoveByDirection.get_moves(self, board, self.directions, self.NOT_KING)


class Rook(Piece):
    """
    A class representing a chess rook.
    """
    directions = [Square(1, 0), Square(-1, 0), Square(0, 1), Square(0, -1)]
    NOT_KING = 1

    def get_available_moves(self, board):
        return MoveByDirection.get_moves(self, board, self.directions, self.NOT_KING)


class Queen(Piece):
    """
    A class representing a chess queen.
    """
    directions = [Square(1, 0), Square(-1, 0), Square(0, 1), Square(0, -1),
                 Square(1, 1), Square(-1, 1), Square(-1, -1), Square(1, -1)]
    NOT_KING = 1

    def get_available_moves(self, board):
        return MoveByDirection.get_moves(self, board, self.directions, self.NOT_KING)


class King(Piece):
    """
    A class representing a chess king.
    """
    directions = [Square(1, 0), Square(-1, 0), Square(0, 1), Square(0, -1),
                  Square(1, 1), Square(-1, 1), Square(-1, -1), Square(1, -1)]
    NOT_KING = 0

    def get_available_moves(self, board):
        return MoveByDirection.get_moves(self, board, self.directions, self.NOT_KING)