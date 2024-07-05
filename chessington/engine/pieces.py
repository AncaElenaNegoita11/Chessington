from __future__ import annotations
from abc import ABC, abstractmethod

from chessington.engine import board
from chessington.engine.data import Player, Square
from typing import TYPE_CHECKING, List

import copy

if TYPE_CHECKING:
    from chessington.engine.board import Board


class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player: Player):
        self.player = player
        self.moved = 0
        self.last_moved = 0

    def piece_moved(self, moves):
        self.moved += 1
        self.last_moved = moves

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
    EN_PASSANT_WHITE = 4
    EN_PASSANT_BLACK = 3

    def get_moves_by_player_color(self):
        move_forward = 1 if self.player == Player.WHITE else -1
        row_first_time_move = self.WHITE_PAWN_LINE if self.player == Player.WHITE else self.BLACK_PAWN_LINE
        row_en_passant = self.EN_PASSANT_WHITE if self.player == Player.WHITE else self.EN_PASSANT_BLACK
        return move_forward, row_first_time_move, row_en_passant

    def first_time_move(self, current_square, row_first_time_move, move_forward, board, list_moves):
        # Verify if it is the first time the pawn moves
        if current_square.row == row_first_time_move:
            square_two_spaces_in_front = Square.at(current_square.row + move_forward * self.FORWARD_TWO_SPACES,
                                                   current_square.col)
            # Can move two squares forward
            if in_bounds(square_two_spaces_in_front) and not board.get_piece(square_two_spaces_in_front):
                list_moves.append(square_two_spaces_in_front)

    def verify_attack_different_color(self, piece):
        return self.player != piece.player

    def attack_diagonally(self, square_diagonal, board, list_moves):
        if in_bounds(square_diagonal):
            diagonal_piece_left = board.get_piece(square_diagonal)
            if diagonal_piece_left and self.verify_attack_different_color(diagonal_piece_left):
                list_moves.append(square_diagonal)

    def verify_attack_diagonally(self, current_square, move_forward, board, list_moves):
        # Attack diagonally (2 spaces possible)
        square_diagonal_left = Square.at(current_square.row + move_forward, current_square.col + self.LEFT)
        square_diagonal_right = Square.at(current_square.row + move_forward, current_square.col + self.RIGHT)

        # Can't attack same color and if a piece isn't there
        self.attack_diagonally(square_diagonal_left, board, list_moves)
        self.attack_diagonally(square_diagonal_right, board, list_moves)

    def en_passant(self, square, board, list_moves, direction):
        piece = board.get_piece(square)
        if piece and piece.moved == 1 and board.moves == piece.last_moved + 1:
            square_diagonal = Square.at(square.row + direction, square.col)
            list_moves.append(square_diagonal)

    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        list_moves = []
        move_forward, row_first_time_move, row_en_passant = self.get_moves_by_player_color()

        square_in_front = Square.at(current_square.row + move_forward, current_square.col)
        # Can move forward at least once
        if in_bounds(square_in_front):
            if not board.get_piece(square_in_front):
                list_moves.append(square_in_front)
                # Verify first time move of pawn
                self.first_time_move(current_square, row_first_time_move, move_forward, board, list_moves)
            # Verify attack diagonally
            self.verify_attack_diagonally(current_square, move_forward, board, list_moves)

        # En passant
        if current_square.row == row_en_passant:
            square_left = Square.at(current_square.row, current_square.col + self.LEFT)
            if in_bounds(square_left):
                self.en_passant(square_left, board, list_moves, move_forward)
            square_right = Square.at(current_square.row, current_square.col + self.RIGHT)
            if in_bounds(square_right):
                self.en_passant(square_right, board, list_moves, move_forward)

        return list_moves


FIRST_STEP = 1


def in_bounds(move) -> bool:
    return move.row in range(0, 8) and move.col in range(0, 8)


def get_position(current_square, current_piece, board, list_moves, step, direction):
    next_square = Square.at(current_square.row + direction.row * step,
                            current_square.col + direction.col * step)
    if in_bounds(next_square):
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


def get_moves(current_piece, board, directions, not_king_or_knight):
    current_square = board.find_piece(current_piece)
    list_moves = []
    for direction in directions:
        continue_moves = get_position(current_square, current_piece, board, list_moves,
                                      FIRST_STEP, direction)
        if not_king_or_knight and continue_moves:
            step = 2
            while True:
                continue_moves = get_position(current_square, current_piece, board,
                                              list_moves, step, direction)
                if not continue_moves:
                    break
                step += 1

    return list_moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """
    directions = [Square(1, -2), Square(2, -1), Square(2, 1), Square(1, 2),
                  Square(-1, -2), Square(-2, -1), Square(-2, 1), Square(-1, 2)]
    NOT_KING_OR_KNIGHT = 0

    def get_available_moves(self, board):
        return get_moves(self, board, self.directions, self.NOT_KING_OR_KNIGHT)


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """
    directions = [Square(1, 1), Square(-1, 1), Square(-1, -1), Square(1, -1)]
    NOT_KING_OR_KNIGHT = 1

    def get_available_moves(self, board):
        return get_moves(self, board, self.directions, self.NOT_KING_OR_KNIGHT)


class Rook(Piece):
    """
    A class representing a chess rook.
    """
    directions = [Square(1, 0), Square(-1, 0), Square(0, 1), Square(0, -1)]
    NOT_KING_OR_KNIGHT = 1

    def get_available_moves(self, board):
        return get_moves(self, board, self.directions, self.NOT_KING_OR_KNIGHT)


class Queen(Piece):
    """
    A class representing a chess queen.
    """
    directions = [Square(1, 0), Square(-1, 0), Square(0, 1), Square(0, -1),
                  Square(1, 1), Square(-1, 1), Square(-1, -1), Square(1, -1)]
    NOT_KING_OR_KNIGHT = 1

    def get_available_moves(self, board):
        return get_moves(self, board, self.directions, self.NOT_KING_OR_KNIGHT)


class King(Piece):
    """
    A class representing a chess king.
    """
    directions = [Square(1, 0), Square(-1, 0), Square(0, 1), Square(0, -1),
                  Square(1, 1), Square(-1, 1), Square(-1, -1), Square(1, -1)]
    NOT_KING_OR_KNIGHT = 0

    def is_attacked(self, board, current_square):
        # Needs modularization
        for row in range(0, 8):
            for col in range(0, 8):
                selected_square = Square.at(row, col)
                selected_piece = board.get_piece(selected_square)
                if selected_piece and selected_piece.player != self.player:
                    if type(selected_piece) is King:
                        if abs(selected_square.row - current_square.row) <= 1 and abs(
                                selected_square.col - current_square.col) <= 1:
                            return True
                    elif type(selected_piece) is Pawn:
                        previous_square = board.find_piece(self)
                        board.set_piece(previous_square, board.get_piece(current_square))
                        board.set_piece(current_square, self)

                        list_moves_available = selected_piece.get_available_moves(board)
                        for available_move in list_moves_available:
                            if available_move.row == current_square.row and \
                                    available_move.col == current_square.col:
                                board.set_piece(current_square, board.get_piece(previous_square))
                                board.set_piece(previous_square, self)
                                return True
                        board.set_piece(current_square, board.get_piece(previous_square))
                        board.set_piece(previous_square, self)

                    else:
                        list_moves_available = selected_piece.get_available_moves(board)
                        for available_move in list_moves_available:
                            if available_move.row == current_square.row and \
                                    available_move.col == current_square.col:
                                return True
        return False

    def get_available_moves(self, board):
        list_moves_available = get_moves(self, board, self.directions, self.NOT_KING_OR_KNIGHT)
        for square in list_moves_available:
            print(square.row, square.col)
        return [square for square in list_moves_available if not self.is_attacked(board, square)]
