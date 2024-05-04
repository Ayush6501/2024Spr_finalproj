from collections import defaultdict


class ThreeMusketeers:
    """
    ThreeMusketeers Puzzle Workhorse class to implement all the moves and checks
    """
    def __init__(self, opp: str, diff: int):
        self.user = opp     # The user's character, either musketeer or enemy
        self.difficulty = diff * 2      # The depth of the tree
        self.player = 'M'       # Player with the first move
        self.board = [['W', 'S', 'S', 'S', 'M'],        # The game board
                      ['S', 'S', 'S', 'S', 'S'],
                      ['S', 'S', 'M', 'S', 'S'],
                      ['S', 'S', 'S', 'S', 'S'],
                      ['M', 'S', 'S', 'S', 'S']]
        self.debug_board = [['W', ' ', 'S', 'S', 'M'],  # A board to help with debugging
                            ['S', ' ', 'S', ' ', 'S'],
                            ['S', ' ', 'M', ' ', ' '],
                            ['S', ' ', 'S', ' ', 'S'],
                            ['M', 'S', 'S', ' ', ' ']]
        self.lost_board = [['W', ' ', 'M', '', ' '],    # Another board to help with debugging
                           ['S', ' ', ' ', ' ', 'S'],
                           [' ', ' ', 'M', ' ', ' '],
                           [' ', ' ', 'S', ' ', 'S'],
                           ['S', ' ', 'M', ' ', ' ']]
        self.musketeers_position = defaultdict()        # Dictionary to track the musketeer's position
        self.winner = None      # Variable to track the winner

    def print_board(self) -> None:
        """
        Prints the game board
        :return: None
        >>> game = ThreeMusketeers('M', 1)
        >>> game.print_board()
        <BLANKLINE>
            0|   1|   2|   3|   4
        0 ['W', 'S', 'S', 'S', 'M']
        1 ['S', 'S', 'S', 'S', 'S']
        2 ['S', 'S', 'M', 'S', 'S']
        3 ['S', 'S', 'S', 'S', 'S']
        4 ['M', 'S', 'S', 'S', 'S']
        <BLANKLINE>
        """
        c = 0
        print()
        print('    0|   1|   2|   3|   4')
        for row in self.board:
            print(str(c) + ' ' + str(row))
            c += 1
        print()
        return

    def get_musketeers(self) -> None:
        """
        Returns the musketeer's position on the board
        Time Complexity: O(N), where N is the size of the board
        :return: None
        >>> game = ThreeMusketeers('M', 1)
        >>> game.get_musketeers()
        >>> print(game.musketeers_position)
        defaultdict(None, {1: (0, 4), 2: (2, 2), 3: (4, 0)})
        """
        num = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 'M':
                    self.musketeers_position[num] = (i, j)
                    num += 1

    def are_moves_available(self, board=None):
        """
        Checks if the board has any available moves for the musketeers
        :param board: if None the class board will be checked, else the dummy board will be checked (minimax)
        :return: True if moves are available, else False
        >>> game = ThreeMusketeers('M', 1)
        >>> game.get_musketeers()
        >>> game.are_moves_available()
        True
        """
        offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        if board is None:
            for _, musketeer in self.musketeers_position.items():
                musk = musketeer
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

    def generate_valid_moves(self, player: bool) -> dict:
        """
        Generates the valid moves for the musketeers as well as the enemy
        Time Complexity: O(N), N is the size of the board
        :param player: Character to generate the moves for
        :return: Moves as a dict
        >>> game = ThreeMusketeers('M', 1)
        >>> game.get_musketeers()
        >>> test_moves = game.generate_valid_moves(True)
        >>> test_moves.keys()
        dict_keys([1, 2, 3])
        """
        moves = defaultdict(lambda: [])
        offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        extended_offsets = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        if player:
            for musketeer, move in self.musketeers_position.items():
                pos = move
                for offset in offsets:
                    if 0 <= pos[0] + offset[0] < 5 and 0 <= pos[1] + offset[1] < 5:
                        if self.board[pos[0] + offset[0]][pos[1] + offset[1]] in ['S', 'W']:
                            moves[musketeer].append((pos[0] + offset[0], pos[1] + offset[1]))
        else:
            w = None
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == ' ':
                        for offset in offsets:
                            if 0 <= i + offset[0] < 5 and 0 <= j + offset[1] < 5:
                                if self.board[i + offset[0]][j + offset[1]] not in ['M', ' ']:
                                    moves[(i, j)].append((i + offset[0], j + offset[1]))
                    elif self.board[i][j] == 'W':
                        w = (i, j)
            if w is not None:
                for offset in extended_offsets:
                    if 0 <= w[0] + offset[0] < 5 and 0 <= w[1] + offset[1] < 5:
                        if self.board[w[0] + offset[0]][w[1] + offset[1]] == ' ':
                            moves[(w[0] + offset[0], w[1] + offset[1])].append((w[0], w[1]))

        return moves

    def make_move(self, src: tuple, dest: tuple, index: int, is_musketeer: bool) -> None:
        """
        Makes a move on the board for both the characters
        :param src: Source cell
        :param dest: Destination cell
        :param index: helper to change the index of the musketeer in the musketeers position dict
        :param is_musketeer: Boolean value to indicate if the character is a musketeer or not
        :return: None
        >>> game = ThreeMusketeers('M', 1)
        >>> game.get_musketeers()
        >>> game.make_move((0, 4), (0, 3), 1, True)
        >>> game.print_board()
        <BLANKLINE>
            0|   1|   2|   3|   4
        0 ['W', 'S', 'S', 'M', ' ']
        1 ['S', 'S', 'S', 'S', 'S']
        2 ['S', 'S', 'M', 'S', 'S']
        3 ['S', 'S', 'S', 'S', 'S']
        4 ['M', 'S', 'S', 'S', 'S']
        <BLANKLINE>
        """
        if is_musketeer:
            self.board[dest[0]][dest[1]] = 'M'
            self.board[src[0]][src[1]] = ' '
            self.musketeers_position[index] = (dest[0], dest[1])
        else:
            if self.board[src[0]][src[1]] == 'W':
                self.board[dest[0]][dest[1]] = 'W'
                self.board[src[0]][src[1]] = ' '
            else:
                self.board[dest[0]][dest[1]] = 'S'
                self.board[src[0]][src[1]] = ' '
        return

    def did_enemy_win(self) -> bool:
        """
        Checks if the enemy wins the game i.e., the musketeers have no available moves
        Time Complexity: O(1)
        :return: True if enemy wins, else False
        >>> game = ThreeMusketeers('M', 1)
        >>> game.get_musketeers()
        >>> game.did_enemy_win()
        False
        >>> game.board = game.lost_board
        >>> game.get_musketeers()
        >>> game.did_enemy_win()
        True
        """
        pos = list(self.musketeers_position.values())
        if (pos[0][0] == pos[1][0] == pos[2][0]) or (pos[0][1] == pos[1][1] == pos[2][1]):
            return True
        return False

    @staticmethod
    def get_enemy_positions(board: list[list]) -> list:
        """
        Returns a list of all enemy positions on the board for the minimax function
        :param board: A representation of the game board.
        :return: A list of all enemy positions
        >>> game = ThreeMusketeers('M', 1)
        >>> game.get_enemy_positions(game.lost_board)
        [(0, 0), (1, 0), (1, 4), (3, 2), (3, 4), (4, 0)]
        """
        enemy = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 'S' or board[i][j] == 'W':
                    enemy.append((i, j))
        return enemy

    @staticmethod
    def get_musk_positions(board: list[list]) -> list:
        """
        Returns a list of all musketeer positions on the board for the minimax function
        :param board: A representation of the game board.
        :return: A list of all musketeer positions
        >>> game = ThreeMusketeers('M', 1)
        >>> game.get_musk_positions(game.lost_board)
        [(0, 2), (2, 2), (4, 2)]
        """
        pos = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 'M':
                    pos.append((i, j))
        return pos

    @staticmethod
    def count_available_squares(board: list[list], is_musketeer: bool) -> int:
        """
        Counts the number of available/empty squares for the minimax function
        :param board: A representation of the game board.
        :param is_musketeer: Bool to indicate if the character is a musketeer or not
        :return: Count of available squares
        >>> game = ThreeMusketeers('M', 1)
        >>> game.count_available_squares(game.board, True)
        0
        """
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

    def calculate_average_distance(self, board: list[list]) -> int:
        """
        Calculates the distance between the musketeers and the enemy for the minimax function
        :param board: A representation of the game board.
        :return: Sum of distance to all the enemy
        >>> game = ThreeMusketeers('M', 1)
        >>> game.calculate_average_distance(game.lost_board)
        62
        """
        enemy_proximity = 0
        for enemy in self.get_enemy_positions(board):  # Get positions of all enemy pieces
            for musketeer in self.get_musk_positions(board):
                distance = abs(enemy[0] - musketeer[0]) + abs(enemy[1] - musketeer[1])  # Manhattan distance
                enemy_proximity += distance
        return enemy_proximity

    def count_musketeers_in_corners(self, board: list[list]) -> int:
        """
        Counts the number of musketeers in the corners of the board
        :param board: A representation of the game board.
        :return: Count of musketeers in the corners of the board
        >>> game = ThreeMusketeers('M', 1)
        >>> game.count_musketeers_in_corners(game.board)
        2
        """
        corner_score = 0
        for musketeer in self.get_musk_positions(board):
            if musketeer in [(0, 0), (4, 0), (4, 4), (0, 4)]:
                corner_score += 1
        return corner_score

    def evaluate(self, board: list[list], is_musketeer: bool) -> int:
        """
        Heuristic evaluation function for Three Musketeers considering refined factors.
        :param board: A representation of the game board.
        :param is_musketeer: Boolean indicating if evaluating for Musketeers (True) or Enemies (False).
        :return: A score representing the board state's favourability for the given player.
        >>> game = ThreeMusketeers('M', 1)
        >>> game.evaluate(game.debug_board, True)
        64
        >>> game.evaluate(game.debug_board, False)
        -18
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

    # noinspection PyTypeChecker
    @staticmethod
    def make_minimax_move(board: list[list], pos: tuple, move: tuple, is_musketeer: bool) -> list[list]:
        """
        Make a move on the minimax board and return the new board
        :param board: A representation of the game board.
        :param pos: Source cell
        :param move: Destination cell
        :param is_musketeer: Boolean indicating if evaluating for Musketeers (True) or Enemies (False).
        :return: Updated board
        """
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

    def generate_valid_moves_minimax(self, board: list[list], player: bool) -> dict:
        """
        Function to generate valid moves for the given player within the minimax function.
        :param board: A representation of the game board.
        :param player: 'M' or 'E' for musketeer or enemy respectively.
        :return: a dictionary of the valid moves for the given player.
        """
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

    def minimax(self, board: list[list], depth: int, is_musketeer: bool,
                alpha: float = float('-inf'), beta: float = float('inf')) -> tuple:
        """
        Minimax function with player-specific heuristic for Three Musketeers.
        Time Complexity: O(m^depth), where m is the number of valid moves.
        :param board: A representation of the game board.
        :param depth: Current depth in the search tree.
        :param is_musketeer: Boolean indicating if calculating for Musketeers (True) or Enemies (False).
        :param alpha: Alpha value for alpha-beta pruning.
        :param beta: Beta value for alpha-beta pruning.
        :return: A tuple containing the best score and the corresponding move.
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
