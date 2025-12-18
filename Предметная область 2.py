import math

class AlphaBeta:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
    
    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or self.is_terminal(board):
            return self.evaluate(board)
        
        if maximizing:
            value = -math.inf
            for move in self.get_moves(board):
                new_board = self.make_move(board, move, 'X')
                value = max(value, self.minimax(new_board, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # beta-отсечение
            return value
        else:
            value = math.inf
            for move in self.get_moves(board):
                new_board = self.make_move(board, move, 'O')
                value = min(value, self.minimax(new_board, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # alpha-отсечение
            return value
    
    def find_best_move(self, board):
        best_val = -math.inf
        best_move = None
        for move in self.get_moves(board):
            new_board = self.make_move(board, move, 'X')
            move_val = self.minimax(new_board, self.max_depth-1, -math.inf, math.inf, False)
            if move_val > best_val:
                best_val = move_val
                best_move = move
        return best_move
    
    # Вспомогательные методы
    def is_terminal(self, board): 
        return False
    
    def evaluate(self, board): 
        return 0
    
    def get_moves(self, board): 
        return []
    
    def make_move(self, board, move, player): 
        return board


class TicTacToeAB(AlphaBeta):
    def is_terminal(self, board):
        # Проверка победы или ничьи
        lines = [
            board[:3], board[3:6], board[6:],  # строки
            board[0:7:3], board[1:8:3], board[2:9:3],  # столбцы
            board[0:9:4], board[2:7:2]  # диагонали
        ]
        
        for line in lines:
            if all(cell == 'X' for cell in line):
                return True
            if all(cell == 'O' for cell in line):
                return True
        
        # Ничья (все клетки заполнены)
        return all(cell != ' ' for cell in board)
    
    def evaluate(self, board):
        # +10 за победу X, -10 за победу O, 0 в остальных случаях
        lines = [
            board[:3], board[3:6], board[6:],  # строки
            board[0:7:3], board[1:8:3], board[2:9:3],  # столбцы
            board[0:9:4], board[2:7:2]  # диагонали
        ]
        
        for line in lines:
            if all(cell == 'X' for cell in line):
                return 10
            if all(cell == 'O' for cell in line):
                return -10
        return 0
    
    def get_moves(self, board):
        return [i for i, cell in enumerate(board) if cell == ' ']
    
    def make_move(self, board, move, player):
        new_board = list(board)
        new_board[move] = player
        return tuple(new_board)


# Использование
if __name__ == "__main__":
    game = TicTacToeAB(max_depth=9)
    board = (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')  # пустая доска 3x3
    best_move = game.find_best_move(board)
    print(f"Лучший ход для X: позиция {best_move}")
    print(f"(0 1 2)")
    print(f"(3 4 5)")
    print(f"(6 7 8)")