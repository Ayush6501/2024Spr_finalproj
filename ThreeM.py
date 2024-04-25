from collections import defaultdict


class ThreeMusketeers:
    def __init__(self, opp):

        self.opponent = opp
        self.player = 'M'
        self.board = [['W', 'S', 'S', 'S', 'M'],
                      ['S', 'S', 'S', 'S', 'S'],
                      ['S', 'S', 'M', 'S', 'S'],
                      ['S', 'S', 'S', 'S', 'S'],
                      ['M', 'S', 'S', 'S', 'S']]
        self.musketeers_position = defaultdict(lambda: [])
        self.winner = None

    def print_board(self):
        print()
        for row in self.board:
            print(row)
        print()
        return

    def get_musketeers(self):
        num = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 'M':
                    self.musketeers_position[num].append((i, j))
                    num += 1

    def is_winner(self):
        pass

    def are_moves_available(self, board=None):
        offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        if board is None:
            self.get_musketeers()
            for _, musketeer in self.musketeers_position.items():
                musk = musketeer[0]
                for offset in offsets:
                    if 0 <= musk[0] + offset[0] < 5 and 0 <= musk[1] + offset[1] < 5:
                        if self.board[musk[0] + offset[0]][musk[1] + offset[1]] != ' ':
                            return True
            return False
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 'M':
                        for offset in offsets:
                            if 0 <= i + offset[0] < 5 and 0 <= j + offset[1] < 5:
                                if board[i + offset[0]][j + offset[1]] != ' ':
                                    return True
            return False

    def generate_valid_moves(self, player):
        moves = defaultdict(lambda: [])
        offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        if player:
            for musketeer, move in self.musketeers_position.items():
                pos = move[0]
                for offset in offsets:
                    if 0 <= pos[0] + offset[0] < 5 and 0 <= pos[1] + offset[1] < 5:
                        if self.board[pos[0] + offset[0]][pos[1] + offset[1]] in ['S', 'W']:
                            moves[musketeer].append((pos[0] + offset[0], pos[1] + offset[1]))
        else:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == ' ':
                        for offset in offsets:
                            if 0 <= i + offset[0] < 5 and 0 <= j + offset[1] < 5:
                                if self.board[i + offset[0]][j + offset[1]] != 'M':
                                    moves[(i, j)].append((i + offset[0], j + offset[1]))
        return moves

    def move_musketeer(self, player, player_num, index, move):
        next_move = move[player_num][index - 1]
        print(next_move)
        # Place M at the next move on the board
        self.board[next_move[0]][next_move[1]] = player
        # Replace the old M on the board with a blank space
        old_position = self.musketeers_position[player_num][0]
        self.board[old_position[0]][old_position[1]] = ' '
        # update musketeers position
        self.musketeers_position[player_num][0] = (next_move[0], next_move[1])
        self.print_board()
        return

    def move_enemy(self, space, enemy):
        self.board[space[0]][space[1]] = 'S'
        self.board[enemy[0]][enemy[1]] = ' '
        self.print_board()
        return

    def did_enemy_win(self):
        pos = list(self.musketeers_position.values())
        if (pos[0][0][0] == pos[1][0][0] == pos[2][0][0]) or (pos[0][0][1] == pos[1][0][1] == pos[2][0][1]):
            return True
        return False

    def is_terminal(self):
        if self.are_moves_available():
            return True
        return False

    @staticmethod
    def get_enemy_positions(board):
        enemy = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 'S' or board[i][j] == 'W':
                    enemy.append((i, j))
        return enemy

    @staticmethod
    def get_musk_positions(board):
        pos = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 'M':
                    pos.append((i, j))
        return pos

    @staticmethod
    def count_available_squares(board, is_musketeer):
        empty = []
        if is_musketeer:
            offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 'M':
                        for offset in offsets:
                            if 0 <= i + offset[0] < 5 and 0 <= j + offset[1] < 5:
                                if board[i + offset[0]][j + offset[1]] == ' ':
                                    empty.append((i + offset[0], j + offset[1]))
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == ' ':
                        empty.append((i, j))
        return len(empty)

    def calculate_average_distance(self, board):
        enemy_proximity = 0
        for enemy in self.get_enemy_positions(board):  # Get positions of all enemy pieces
            for musketeer in self.get_musk_positions(board):
                distance = abs(enemy[0] - musketeer[0]) + abs(enemy[1] - musketeer[1])  # Manhattan distance
                enemy_proximity += distance
        return enemy_proximity

    def count_musketeers_in_corners(self, board):
        corner_score = 0
        for musketeer in self.get_musk_positions(board):
            if musketeer in [(0, 0), (4, 0), (4, 4), (0, 4)]:
                corner_score += 1
        return corner_score

    def evaluate(self, board, is_musketeer):
        """
        Heuristic evaluation function for Three Musketeers considering refined factors.

        Args:
            board: A representation of the game board.
            is_musketeer: Boolean indicating if evaluating for Musketeers (True) or Enemies (False).

        Returns:
            A score representing the board state's favorability for the given player.
        """
        if is_musketeer:
            enemy_count = len(self.get_enemy_positions(board))  # Count Enemies
            open_squares = self.count_available_squares(board, True)  # Count available squares for movement
            avg_musketeer_distance = self.calculate_average_distance(board)
            corner_penalty = self.count_musketeers_in_corners(board) * 2

            # Prioritize less Enemies, open spaces, and distance between Musketeers
            return -enemy_count * 5 + open_squares + avg_musketeer_distance - corner_penalty
        else:
            enemy_count = len(self.get_enemy_positions(board))  # Count Enemies
            # Favor fewer Musketeers and more potential traps (adjacent squares to Musketeers)
            enemy_adjacent_squares = self.count_available_squares(board, False)
            empty_adjacent_penalty = self.count_available_squares(board, True) * 2

            return enemy_count * -2 + enemy_adjacent_squares - empty_adjacent_penalty

    @staticmethod
    def make_minimax_move(board, pos, move, is_musketeer):
        if is_musketeer:
            pass
            # replace move with 'M'
            board[move[0]][move[1]] = 'M'
            # replace pos with ' '
            board[pos[0]][pos[1]] = ' '
        else:
            # replace pos with S
            board[pos[0]][pos[1]] = 'S'
            # replace move with ' '
            board[move[0]][move[1]] = ' '
        return board

    def generate_valid_moves_minimax(self, board, player):
        moves = defaultdict(lambda: [])
        offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        if player:
            for musketeer in self.get_musk_positions(board):
                for offset in offsets:
                    if 0 <= musketeer[0] + offset[0] < 5 and 0 <= musketeer[1] + offset[1] < 5:
                        if self.board[musketeer[0] + offset[0]][musketeer[1] + offset[1]] in ['S', 'W']:
                            moves[tuple(musketeer)].append((musketeer[0] + offset[0], musketeer[1] + offset[1]))
        else:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == ' ':
                        for offset in offsets:
                            if 0 <= i + offset[0] < 5 and 0 <= j + offset[1] < 5:
                                if self.board[i + offset[0]][j + offset[1]] != 'M':
                                    moves[(i, j)].append((i + offset[0], j + offset[1]))
        return moves

    def minimax(self, board, depth, is_musketeer, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax function with player-specific heuristic for Three Musketeers.

        Args:
            board: A representation of the game board.
            depth: Current depth in the search tree.
            alpha: Alpha value for alpha-beta pruning.
            beta: Beta value for alpha-beta pruning.
            is_musketeer: Boolean indicating if calculating for Musketeers (True) or Enemies (False).

        Returns:
            A tuple containing the best score and the corresponding move.
        """
        # Check for terminal state (win or draw)
        if not self.are_moves_available(board):
            return self.evaluate(board, is_musketeer), None

        # Base case: Reached maximum depth
        if depth == 0:
            return self.evaluate(board, is_musketeer), None

        # Initialize variables
        best_score = float('-inf') if is_musketeer else float('inf')
        best_move = None
        best_position = None

        # Generate all valid moves for the current player
        for pos, moves in self.generate_valid_moves_minimax(board, is_musketeer).items():
            for move in moves:
                # Simulate the move on a copy of the board
                new_board = self.make_minimax_move(board, pos, move, is_musketeer)

                # Recursively evaluate the opponent's move
                score, _ = self.minimax(new_board, depth - 1, not is_musketeer, alpha, beta)

                # Update best move based on player and minimax logic
                if is_musketeer:
                    best_score = max(best_score, score)
                    if score >= best_score:
                        best_move = move
                        best_position = pos
                else:
                    best_score = min(best_score, score)
                    if score <= best_score:
                        best_move = move
                        best_position = pos

                # Alpha-beta pruning
                alpha = max(alpha, best_score) if is_musketeer else min(alpha, best_score)
                if beta <= alpha:
                    break

        return best_score, (best_move, best_position)

    def play_vs_comp(self):
        pass

    def play_vs_human(self):
        pass

    def play_vs_ai(self):
        pass
