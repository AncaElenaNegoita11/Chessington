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

    def get_moves_by_player_color(self):
        move_forward_once = 1
        move_forward_twice = 2
        row_first_time_move_forward_twice = 1
        if self.player == Player.BLACK:
            move_forward_once = -1
            move_forward_twice = -2
            row_first_time_move_forward_twice = 6
        return move_forward_once, move_forward_twice, row_first_time_move_forward_twice

    def in_bounds(self, move) -> bool:
        return move in range(0, 8)

    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        list_moves = []
        move_forward_once, move_forward_twice, row_first_time_move = self.get_moves_by_player_color()

        square_in_front = Square.at(current_square.row + move_forward_once, current_square.col)
        # Can move forward at least once
        if self.in_bounds(square_in_front.row) and not board.get_piece(square_in_front):
            list_moves.append(square_in_front)
            # Verify if it is the first time the pawn moves
            if current_square.row == row_first_time_move:
                square_two_spaces_in_front = Square.at(current_square.row + move_forward_twice, current_square.col)
                # Can move two squares forward
                if self.in_bounds(square_two_spaces_in_front.row) and not board.get_piece(square_two_spaces_in_front):
                    list_moves.append(square_two_spaces_in_front)
            # Attack diagonally (2 spaces possible)
            square_diagonal1 = Square.at(current_square.row + move_forward_once, current_square.col - 1)
            square_diagonal2 = Square.at(current_square.row + move_forward_once, current_square.col + 1)
            diagonal_piece1 = board.get_piece(square_diagonal1)
            diagonal_piece2 = board.get_piece(square_diagonal2)
            if self.in_bounds(square_diagonal1.col) and diagonal_piece1 and self.player != diagonal_piece1.player:
                list_moves.append(square_diagonal1)
            if self.in_bounds(square_diagonal2.col) and diagonal_piece2 and self.player != diagonal_piece2.player:
                list_moves.append(square_diagonal2)
        return list_moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []