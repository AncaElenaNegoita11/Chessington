from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Rook


class TestRook:
    @staticmethod
    def test_rook_can_move_forward():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(0, 7)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(1, 8):
            assert Square.at(i, 7) in moves

    @staticmethod
    def test_rook_can_move_backwards():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(7, 7)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(0, 7):
            assert Square.at(i, 7) in moves

    @staticmethod
    def test_rook_can_move_left():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(2, 7)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(0, 7):
            assert Square.at(2, i) in moves

    @staticmethod
    def test_rook_can_move_right():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(2, 0)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(1, 8):
            assert Square.at(2, i) in moves

    @staticmethod
    def test_rook_can_move_left_and_right():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(5, 5)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(0, 8):
            if i != 5:
                assert Square.at(5, i) in moves

    @staticmethod
    def test_rook_can_move_forward_and_backwards():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(4, 4)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(0, 8):
            if i != 4:
                assert Square.at(i, 4) in moves

    @staticmethod
    def test_rook_cannot_move_outside_left_and_down_border():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(0, 0)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(-1, 0) not in moves
        assert Square.at(0, -1) not in moves

    @staticmethod
    def test_rook_cannot_move_outside_right_and_up_border():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(7, 7)
        board.set_piece(rook_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(7, 8) not in moves
        assert Square.at(8, 7) not in moves

    @staticmethod
    def test_rook_cannot_move_forward_if_piece_of_same_color_in_front():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(0, 7)
        board.set_piece(rook_square, rook)

        obstructing_square = Square.at(1, 7)
        obstruction = Rook(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(1, 8):
            assert Square.at(i, 7) not in moves

    @staticmethod
    def test_rook_cannot_move_backwards_if_piece_of_same_color_in_back():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(5, 5)
        board.set_piece(rook_square, rook)

        obstructing_square = Square.at(4, 5)
        obstruction = Rook(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(0, 5):
            assert Square.at(i, 5) not in moves

    @staticmethod
    def test_rook_cannot_move_left_if_piece_of_same_color_in_left():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(2, 7)
        board.set_piece(rook_square, rook)

        obstructing_square = Square.at(2, 6)
        obstruction = Rook(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(0, 7):
            assert Square.at(2, i) not in moves

    @staticmethod
    def test_rook_cannot_move_right_if_piece_of_same_color_in_right():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(2, 3)
        board.set_piece(rook_square, rook)

        obstructing_square = Square.at(2, 4)
        obstruction = Rook(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(4, 8):
            assert Square.at(2, i) not in moves

    @staticmethod
    def test_rook_attack_forward_if_piece_of_different_color_in_front():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(1, 3)
        board.set_piece(rook_square, rook)

        enemy_square = Square.at(3, 3)
        enemy = Rook(Player.BLACK)
        board.set_piece(enemy_square, enemy)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert enemy_square in moves

    @staticmethod
    def test_rook_attack_backwards_if_piece_of_different_color_in_back():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(5, 5)
        board.set_piece(rook_square, rook)

        enemy_square = Square.at(4, 5)
        enemy = Rook(Player.BLACK)
        board.set_piece(enemy_square, enemy)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert enemy_square in moves

    @staticmethod
    def test_rook_attack_left_if_piece_of_different_color_in_left():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(2, 7)
        board.set_piece(rook_square, rook)

        enemy_square = Square.at(2, 4)
        enemy = Rook(Player.BLACK)
        board.set_piece(enemy_square, enemy)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert enemy_square in moves

    @staticmethod
    def test_rook_attack_right_if_piece_of_different_color_in_right():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(2, 3)
        board.set_piece(rook_square, rook)

        obstructing_square = Square.at(2, 4)
        obstruction = Rook(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        for i in range(4, 8):
            assert Square.at(2, i) not in moves

