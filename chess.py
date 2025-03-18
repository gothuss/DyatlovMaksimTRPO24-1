class Board:
    """Класс, представляющий шахматную доску."""

    def __init__(self, game_type='chess'):
        """Инициализация доски, истории ходов и истории отмененных ходов."""
        self.game_type = game_type
        self.board = self.create_board()
        self.move_history = []
        self.redo_history = []

    def create_board(self):
        if self.game_type == 'chess':
            return [
                ['r', 'w', 'a', 'q', 'k', 'a', 'w', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['R', 'W', 'A', 'Q', 'K', 'A', 'W', 'R']
            ]
        elif self.game_type == 'checkers':
            board = [['.' for _ in range(8)] for _ in range(8)]
            # Черные шашки (сверху)
            for row in range(3):
                for col in range(8):
                    if (row + col) % 2 == 1:
                        board[row][col] = 'b'  # Обычная черная шашка
            # Белые шашки (снизу)
            for row in range(5, 8):
                for col in range(8):
                    if (row + col) % 2 == 1:
                        board[row][col] = 'W'  # Обычная белая шашка
            return board

    def print_board(self, highlight=None):
        """Выводит доску в терминал с подсветкой указанных клеток.

        Args:
            highlight (list): Список координат клеток для подсветки.
        """
        if highlight is None:
            highlight = []
        print("    Black")
        print("    A B C D E F G H")
        print()
        for i in range(8):
            print(8 - i, end='   ')
            for j in range(8):
                if (i, j) in highlight:
                    print(f"\033[46m{self.board[i][j]}\033[0m", end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print(' ', 8 - i)
        print()
        print("    A B C D E F G H")
        print("    White")
        print('-----------------------------')

    def parse_position(self, pos):
        """Преобразует шахматную нотацию (например, 'e2') в координаты доски.

        Args:
            pos (str): Позиция в шахматной нотации (например, 'e2').

        Returns:
            tuple: Координаты (строка, столбец).
        """
        col = ord(pos[0].lower()) - ord('a')
        row = 8 - int(pos[1])
        return row, col

    def make_move(self, start, end):
        """Выполняет ход фигуры с начальной позиции на конечную.

        Args:
            start (str): Начальная позиция (например, 'e2').
            end (str): Конечная позиция (например, 'e4').
        """
        start_row, start_col = self.parse_position(start)
        end_row, end_col = self.parse_position(end)
        piece = self.board[start_row][start_col]
        captured_piece = self.board[end_row][end_col]

        if abs(start_row - end_row) == 2:  # Если это взятие
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            captured_piece = self.board[mid_row][mid_col]
            self.board[mid_row][mid_col] = '.'

        self.move_history.append((start, end, piece, captured_piece))
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'
        self.redo_history.clear()

        if self.game_type == 'checkers':
            if (piece == 'W' and end_row == 0) or (piece == 'b' and end_row == 7):
                self.board[end_row][end_col] = 'K' if piece.isupper() else 'k'

    def undo_move(self):
        """Отменяет последний ход."""
        if self.move_history:
            start, end, piece, captured_piece = self.move_history.pop()
            start_row, start_col = self.parse_position(start)
            end_row, end_col = self.parse_position(end)
            if abs(start_row - end_row) == 2:  # Восстанавливаем взятую шашку
                mid_row = (start_row + end_row) // 2
                mid_col = (start_col + end_col) // 2
                self.board[mid_row][mid_col] = captured_piece

            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = captured_piece

            self.redo_history.append((start, end, piece, captured_piece))

    def redo_move(self):
        """Повторяет последний отмененный ход."""
        if self.redo_history:
            start, end, piece, captured_piece = self.redo_history.pop()
            start_row, start_col = self.parse_position(start)
            end_row, end_col = self.parse_position(end)
            if abs(start_row - end_row) == 2:  # Удаляем взятую шашку при redo
                mid_row = (start_row + end_row) // 2
                mid_col = (start_col + end_col) // 2
                self.board[mid_row][mid_col] = '.'

            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = '.'

            self.move_history.append((start, end, piece, captured_piece))


class Piece:
    """Базовый класс для шахматной фигуры."""

    def __init__(self, color, position):
        """Инициализация фигуры.

        Args:
            color (str): Цвет фигуры ('white' или 'black').
            position (str): Позиция фигуры на доске (например, 'e2').
        """
        self.color = color
        self.position = position

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход допустимым.

        Args:
            board (Board): Шахматная доска.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        pass

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для фигуры.

        Args:
            board (Board): Шахматная доска.

        Returns:
            list: Список возможных ходов.
        """
        pass

class Checker(Piece):
    """Класс, представляющий обычную шашку."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход шашки допустимым."""
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        direction = -1 if self.color == 'white' else 1  # Направление движения

        # Обычный ход
        if abs(start_col - end_col) == 1 and end_row - start_row == direction:
            return board.board[end_row][end_col] == '.'

        # Взятие (любой фигуры)
        if abs(start_col - end_col) == 2 and end_row - start_row == 2 * direction:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            return (
                board.board[mid_row][mid_col] != '.' and  # Любая фигура в середине
                board.board[end_row][end_col] == '.'      # Клетка назначения пуста
            )

        return False
    
    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для шашки."""
        moves = []
        start_row, start_col = board.parse_position(self.position)
        direction = -1 if self.color == 'white' else 1

        # Обычные ходы
        for col_offset in [-1, 1]:
            new_row, new_col = start_row + direction, start_col + col_offset
            if 0 <= new_row < 8 and 0 <= new_col < 8 and board.board[new_row][new_col] == '.':
                moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")

        # Взятия
        for col_offset in [-2, 2]:
            new_row, new_col = start_row + 2 * direction, start_col + col_offset
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                mid_row, mid_col = start_row + direction, start_col + col_offset // 2
                if (board.board[mid_row][mid_col] != '.' and
                        board.board[mid_row][mid_col].islower() != (self.color == 'white') and
                        board.board[new_row][new_col] == '.'):
                    moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")

        return moves

class KingChecker(Piece):
    """Класс, представляющий дамку."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход дамки допустимым."""
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step
        captured = 0
        while row != end_row:
            if board.board[row][col] != '.':
                if captured or board.board[row][col].islower() == (self.color == 'white'):
                    return False
                captured += 1
            row += row_step
            col += col_step
        return board.board[end_row][end_col] == '.' and captured <= 1

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для дамки."""
        moves = []
        start_row, start_col = board.parse_position(self.position)
        for row_step, col_step in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = start_row + row_step, start_col + col_step
            captured = 0
            while 0 <= row < 8 and 0 <= col < 8:
                if board.board[row][col] != '.':
                    if captured or board.board[row][col].islower() == (self.color == 'white'):
                        break
                    captured += 1
                    row += row_step
                    col += col_step
                    if 0 <= row < 8 and 0 <= col < 8 and board.board[row][col] == '.':
                        moves.append(f"{chr(col + ord('a'))}{8 - row}")
                    break
                moves.append(f"{chr(col + ord('a'))}{8 - row}")
                row += row_step
                col += col_step
        return moves

class Pawn(Piece):
    """Класс, представляющий пешку."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход пешки допустимым.

        Args:
            board (Board): Шахматная доска.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        direction = -1 if self.color == 'white' else 1  # Направление движения

        # Обычный ход вперед
        if start_col == end_col:
            if start_row + direction == end_row and board.board[end_row][end_col] == '.':
                return True
            if (start_row == 1 or start_row == 6) and start_row + 2 * direction == end_row and board.board[end_row][end_col] == '.' and board.board[start_row + direction][start_col] == '.':
                return True
        # Диагональное взятие
        elif abs(start_col - end_col) == 1 and start_row + direction == end_row:
            if board.board[end_row][end_col] != '.':
                # Проверяем, что фигура на конечной клетке принадлежит противнику
                if (self.color == 'white' and board.board[end_row][end_col].islower()) or (self.color == 'black' and board.board[end_row][end_col].isupper()):
                    return True
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для пешки.

        Args:
            board (Board): Шахматная доска.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)
        direction = -1 if self.color == 'white' else 1
        if 0 <= start_row + direction < 8 and board.board[start_row + direction][start_col] == '.':
            moves.append(f"{chr(start_col + ord('a'))}{8 - (start_row + direction)}")
            if (start_row == 1 or start_row == 6) and board.board[start_row + 2 * direction][start_col] == '.':
                moves.append(f"{chr(start_col + ord('a'))}{8 - (start_row + 2 * direction)}")
        for col_offset in [-1, 1]:
            if 0 <= start_col + col_offset < 8 and 0 <= start_row + direction < 8:
                if board.board[start_row + direction][start_col + col_offset] != '.' and board.board[start_row + direction][start_col + col_offset].islower() != self.color == 'white':
                    moves.append(f"{chr(start_col + col_offset + ord('a'))}{8 - (start_row + direction)}")
        return moves


class Knight(Piece):
    """Класс, представляющий коня."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход коня допустимым.

        Args:
            board (Board): Шахматная доска.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для коня.

        Args:
            board (Board): Шахматная доска.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)
        for row_offset in [-2, -1, 1, 2]:
            for col_offset in [-2, -1, 1, 2]:
                if abs(row_offset) != abs(col_offset):
                    new_row, new_col = start_row + row_offset, start_col + col_offset
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_move(board, f"{chr(new_col + ord('a'))}{8 - new_row}"):
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        return moves


class Bishop(Piece):
    """Класс, представляющий слона."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход слона допустимым.

        Args:
            board (Board): Шахматная доска.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step
            while row != end_row:
                if board.board[row][col] != '.':
                    return False
                row += row_step
                col += col_step
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для слона.

        Args:
            board (Board): Шахматная доска.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)
        for row_step, col_step in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = start_row + row_step, start_col + col_step
            while 0 <= row < 8 and 0 <= col < 8:
                if board.board[row][col] == '.':
                    moves.append(f"{chr(col + ord('a'))}{8 - row}")
                else:
                    if board.board[row][col].islower() != self.color == 'white':
                        moves.append(f"{chr(col + ord('a'))}{8 - row}")
                    break
                row += row_step
                col += col_step
        return moves


class Rook(Piece):
    """Класс, представляющий ладью."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход ладьи допустимым.

        Args:
            board (Board): Шахматная доска.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if start_row == end_row:
            for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if board.board[start_row][col] != '.':
                    return False
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        elif start_col == end_col:
            for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if board.board[row][start_col] != '.':
                    return False
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для ладьи.

        Args:
            board (Board): Шахматная доска.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)
        for row in range(8):
            if row != start_row and self.is_valid_move(board, f"{chr(start_col + ord('a'))}{8 - row}"):
                moves.append(f"{chr(start_col + ord('a'))}{8 - row}")
        for col in range(8):
            if col != start_col and self.is_valid_move(board, f"{chr(col + ord('a'))}{8 - start_row}"):
                moves.append(f"{chr(col + ord('a'))}{8 - start_row}")
        return moves


class Queen(Piece):
    """Класс, представляющий ферзя."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход ферзя допустимым.

        Args:
            board (Board): Шахматная доска.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
            return Rook.is_valid_move(self, board, end) or Bishop.is_valid_move(self, board, end)
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для ферзя.

        Args:
            board (Board): Шахматная доска.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)
        for row in range(8):
            if row != start_row and self.is_valid_move(board, f"{chr(start_col + ord('a'))}{8 - row}"):
                moves.append(f"{chr(start_col + ord('a'))}{8 - row}")
        for col in range(8):
            if col != start_col and self.is_valid_move(board, f"{chr(col + ord('a'))}{8 - start_row}"):
                moves.append(f"{chr(col + ord('a'))}{8 - start_row}")
        for row_step, col_step in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = start_row + row_step, start_col + col_step
            while 0 <= row < 8 and 0 <= col < 8:
                if self.is_valid_move(board, f"{chr(col + ord('a'))}{8 - row}"):
                    moves.append(f"{chr(col + ord('a'))}{8 - row}")
                row += row_step
                col += col_step
        return moves


class King(Piece):
    """Класс, представляющий короля."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход короля допустимым.

        Args:
            board (Board): Шахматная доска.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для короля.

        Args:
            board (Board): Шахматная доска.

        Returns:
            list: Список возможных ходов.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset != 0 or col_offset != 0:
                    new_row, new_col = start_row + row_offset, start_col + col_offset
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_move(board, f"{chr(new_col + ord('a'))}{8 - new_row}"):
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        return moves


class Wizard(Piece):
    """Класс, представляющий волшебника."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход волшебника допустимым."""
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)

        # Ход как конь
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        
        # Ход как король (на одну клетку в любом направлении)
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для волшебника."""
        moves = []
        start_row, start_col = board.parse_position(self.position)
        
        # Ходы как конь
        for row_offset in [-2, -1, 1, 2]:
            for col_offset in [-2, -1, 1, 2]:
                if abs(row_offset) != abs(col_offset):
                    new_row, new_col = start_row + row_offset, start_col + col_offset
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_move(board, f"{chr(new_col + ord('a'))}{8 - new_row}"):
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        
        # Ходы как король
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset != 0 or col_offset != 0:
                    new_row, new_col = start_row + row_offset, start_col + col_offset
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_move(board, f"{chr(new_col + ord('a'))}{8 - new_row}"):
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        
        return moves


class Dragon(Piece):
    """Класс, представляющий дракона."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход дракона допустимым."""
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)

        # Ход как ладья
        if start_row == end_row or start_col == end_col:
            return Rook.is_valid_move(self, board, end)
        
        # Ход как конь (перепрыгивает через одну фигуру)
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для дракона."""
        moves = []
        start_row, start_col = board.parse_position(self.position)
        
        # Ходы как ладья
        for row in range(8):
            if row != start_row and self.is_valid_move(board, f"{chr(start_col + ord('a'))}{8 - row}"):
                moves.append(f"{chr(start_col + ord('a'))}{8 - row}")
        for col in range(8):
            if col != start_col and self.is_valid_move(board, f"{chr(col + ord('a'))}{8 - start_row}"):
                moves.append(f"{chr(col + ord('a'))}{8 - start_row}")
        
        # Ходы как конь
        for row_offset in [-2, -1, 1, 2]:
            for col_offset in [-2, -1, 1, 2]:
                if abs(row_offset) != abs(col_offset):
                    new_row, new_col = start_row + row_offset, start_col + col_offset
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_move(board, f"{chr(new_col + ord('a'))}{8 - new_row}"):
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        
        return moves


class Archer(Piece):
    """Класс, представляющий стрелка."""

    def is_valid_move(self, board, end):
        """Проверяет, является ли ход стрелка допустимым."""
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)

        # Ход как слон
        if abs(start_row - end_row) == abs(start_col - end_col):
            return Bishop.is_valid_move(self, board, end)
        
        # "Стрельба" на две клетки по диагонали
        if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
            return board.board[end_row][end_col] != '.' and board.board[end_row][end_col].islower() != self.color == 'white'
        
        return False

    def get_possible_moves(self, board):
        """Возвращает список возможных ходов для стрелка."""
        moves = []
        start_row, start_col = board.parse_position(self.position)
        
        # Ходы как слон
        for row_step, col_step in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = start_row + row_step, start_col + col_step
            while 0 <= row < 8 and 0 <= col < 8:
                if self.is_valid_move(board, f"{chr(col + ord('a'))}{8 - row}"):
                    moves.append(f"{chr(col + ord('a'))}{8 - row}")
                row += row_step
                col += col_step
        
        # "Стрельба" на две клетки по диагонали
        for row_step, col_step in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            row, col = start_row + row_step, start_col + col_step
            if 0 <= row < 8 and 0 <= col < 8 and self.is_valid_move(board, f"{chr(col + ord('a'))}{8 - row}"):
                moves.append(f"{chr(col + ord('a'))}{8 - row}")
        
        return moves


class Game:
    """Класс, управляющий шахматной игрой."""

    def __init__(self):
        """Инициализация игры."""
        self.board = Board()
        self.turn = 'white'
        self.move_count = 0

    def play(self):
        """Основной цикл игры."""
        while True:
            self.board.print_board()
            print(f"Ход {'белых' if self.turn == 'white' else 'черных'}. Введите ход (например, e2 e4) или команду (back, next, hint, threats, save, load, exit):")
            command = input().strip().lower()

            if command == 'exit':
                break
            elif command == 'back':
                self.board.undo_move()
                self.move_count -= 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif command == 'next':
                self.board.redo_move()
                self.move_count += 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif command.startswith('hint'):
                pos = command.split()[1]
                self.hint(pos)
            elif command.startswith('threats'):
                pos = command.split()[1]
                self.threats(pos)
            elif command.startswith('save'):
                filename = command.split()[1]
                self.save_game(filename)
            elif command.startswith('load'):
                filename = command.split()[1]
                self.load_game(filename)
            else:
                try:
                    start, end = command.split()
                    if self.is_valid_move(start, end):
                        self.board.make_move(start, end)
                        self.move_count += 1
                        self.turn = 'black' if self.turn == 'white' else 'white'
                    else:
                        print("Неверный ход. Повторите попытку.")
                except ValueError:
                    print("Неверный формат команды. Повторите попытку.")

    def is_valid_move(self, start, end):
        """Проверяет, является ли ход допустимым.

        Args:
            start (str): Начальная позиция.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = self.board.parse_position(start)
        end_row, end_col = self.board.parse_position(end)
        piece = self.board.board[start_row][start_col]

        if piece == '.':
            return False

        if piece.lower() == 'p':
            return Pawn('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'h':
            return Knight('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'r':
            return Rook('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'b':
            return Bishop('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'q':
            return Queen('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'k':
            return King('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'w':  # Волшебник
            return Wizard('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'd':  # Дракон
            return Dragon('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'a':  # Стрелок
            return Archer('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)

        return False

    def hint(self, pos):
        """Показывает возможные ходы для фигуры на указанной клетке.

        Args:
            pos (str): Позиция фигуры (например, 'e2').
        """
        row, col = self.board.parse_position(pos)
        piece = self.board.board[row][col]

        if piece == '.':
            print("На этой клетке нет фигуры.")
            return

        if (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
            print("Нельзя получить подсказку для фигуры противника.")
            return

        moves = []
        if piece.lower() == 'p':
            moves = Pawn('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'h':
            moves = Knight('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'r':
            moves = Rook('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'b':
            moves = Bishop('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'q':
            moves = Queen('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'k':
            moves = King('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'w':  # Волшебник
            moves = Wizard('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'd':  # Дракон
            moves = Dragon('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'a':  # Стрелок
            moves = Archer('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)

        if moves:
            print(f"Возможные ходы для фигуры на {pos}: {', '.join(moves)}")
            highlight = [self.board.parse_position(move) for move in moves]
            self.board.print_board(highlight)
        else:
            print(f"Нет возможных ходов для фигуры на {pos}.")

    def threats(self, pos):
        """Показывает, какие фигуры угрожают указанной клетке.

        Args:
            pos (str): Позиция клетки (например, 'e4').
        """
        row, col = self.board.parse_position(pos)
        threats = []

        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece != '.' and piece.islower() != self.board.board[row][col].islower():
                    # Определяем тип фигуры и вызываем get_possible_moves для неё
                    if piece.lower() == 'p':
                        moves = Pawn('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'h':
                        moves = Knight('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'r':
                        moves = Rook('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'b':
                        moves = Bishop('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'q':
                        moves = Queen('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'k':
                        moves = King('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'w':  # Волшебник
                        moves = Wizard('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'd':  # Дракон
                        moves = Dragon('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'a':  # Стрелок
                        moves = Archer('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    
                    # Проверяем, может ли фигура атаковать указанную позицию
                    for move in moves:
                        if self.board.parse_position(move) == (row, col):
                            threats.append((i, j))

        # Выводим результат
        self.board.print_board(threats)
        if threats:
            print(f"Фигура на позиции {pos} под угрозой от следующих фигур:")
            for threat in threats:
                print(f"{self.board.board[threat[0]][threat[1]]} на {chr(threat[1] + ord('a'))}{8 - threat[0]}")
        else:
            print(f"Фигура на позиции {pos} не под угрозой.")

    def save_game(self, filename):
        """Сохраняет текущую партию в файл.

        Args:
            filename (str): Имя файла для сохранения.
        """
        with open(filename, 'w') as file:
            for move in self.board.move_history:
                start, end, piece, captured_piece = move
                start_row, start_col = self.board.parse_position(start)
                end_row, end_col = self.board.parse_position(end)
                start_pos = f"{chr(start_col + ord('a'))}{8 - start_row}"
                end_pos = f"{chr(end_col + ord('a'))}{8 - end_row}"
                full_notation = f"{piece}{start_pos}{end_pos}"
                file.write(f"{full_notation}\n")
        print(f"Партия сохранена в файл {filename}")

    def load_game(self, filename):
        """Загружает партию из файла.

        Args:
            filename (str): Имя файла для загрузки.
        """
        self.board = Board()
        self.turn = 'white'
        self.move_count = 0

        with open(filename, 'r') as file:
            for line in file:
                move = line.strip()
                piece = move[0]
                start_pos = move[1:3]
                end_pos = move[3:5]
                self.board.make_move(start_pos, end_pos)
        print(f"Партия загружена из файла {filename}")
class CheckersGame(Game):
    """Класс, управляющий игрой в шашки."""

    def __init__(self):
        self.board = Board(game_type='checkers')
        self.turn = 'white'
        self.move_count = 0

    def is_valid_move(self, start, end):
        """Проверяет, является ли ход допустимым в шашках."""
        start_row, start_col = self.board.parse_position(start)
        piece = self.board.board[start_row][start_col]
        if piece == '.' or (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
            return False

        checker = Checker('white' if piece.isupper() else 'black', start) if piece in 'Wb' else KingChecker('white' if piece.isupper() else 'black', start)
        return checker.is_valid_move(self.board, end)

    def make_move(self, start, end):
        print(f"\n=== Попытка хода {start} -> {end} ===")
        start_row, start_col = self.board.parse_position(start)
        end_row, end_col = self.board.parse_position(end)
        piece = self.board.board[start_row][start_col]
        print(f"Фигура: {piece}, цвет: {'белый' if piece.isupper() else 'черный'}")

        if abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            print(f"Удаление шашки на позиции {chr(mid_col + ord('a'))}{8 - mid_row}")
            self.board.board[mid_row][mid_col] = '.'

        # Обработка взятия
        if abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            captured = self.board.board[mid_row][mid_col]
            self.board.board[mid_row][mid_col] = '.'  # Удаляем шашку противника
            self.board.move_history.append((start, end, piece, captured))
        else:
            self.board.move_history.append((start, end, piece, None))

        # Перемещение шашки
        self.board.board[start_row][start_col] = '.'
        self.board.board[end_row][end_col] = piece

        # Превращение в дамку
        if (piece == 'W' and end_row == 0) or (piece == 'b' and end_row == 7):
            self.board.board[end_row][end_col] = piece.upper() if self.turn == 'white' else piece.lower()

        self.turn = 'black' if self.turn == 'white' else 'white'

    def hint(self, pos):
        """Показывает возможные ходы для шашки на указанной клетке."""
        row, col = self.board.parse_position(pos)
        piece = self.board.board[row][col]

        if piece == '.':
            print("На этой клетке нет шашки.")
            return
        if (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
            print("Нельзя получить подсказку для шашки противника.")
            return

        checker = Checker('white' if piece.isupper() else 'black', pos) if piece in 'Wb' else KingChecker('white' if piece.isupper() else 'black', pos)
        moves = checker.get_possible_moves(self.board)

        if moves:
            print(f"Возможные ходы для шашки на {pos}: {', '.join(moves)}")
            highlight = [self.board.parse_position(move) for move in moves]
            self.board.print_board(highlight)
        else:
            print(f"Нет возможных ходов для шашки на {pos}.")

    def threats(self, pos):
        """Показывает, какие шашки угрожают указанной клетке."""
        row, col = self.board.parse_position(pos)
        threats = []
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece != '.' and piece.islower() != self.board.board[row][col].islower():
                    checker = Checker('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}") if piece in 'Wb' else KingChecker('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}")
                    moves = checker.get_possible_moves(self.board)
                    if pos in moves:
                        threats.append((i, j))

        self.board.print_board(threats)
        if threats:
            print(f"Клетка {pos} под угрозой от следующих шашек:")
            for threat in threats:
                print(f"{self.board.board[threat[0]][threat[1]]} на {chr(threat[1] + ord('a'))}{8 - threat[0]}")
        else:
            print(f"Клетка {pos} не под угрозой.")

if __name__ == "__main__":
    print("Выберите игру: 1 - Шахматы, 2 - Шашки")
    choice = input().strip()
    if choice == '1':
        game = Game()
    elif choice == '2':
        game = CheckersGame()
    else:
        print("Неверный выбор, запускаются шахматы по умолчанию.")
        game = Game()
    game.play()