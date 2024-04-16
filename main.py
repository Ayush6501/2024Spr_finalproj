class ThreeMusketeers:
    def _init_(self, opponent):
        self.opponent = opponent
        self.board = [['W', 'S', 'S', 'S', 'M'],
                      ['S', 'S', 'S', 'S', 'S'],
                      ['S', 'S', 'M', 'S', 'S'],
                      ['S', 'S', 'S', 'S', 'S'],
                      ['M', 'S', 'S', 'S', 'S'], ]
        self.winner = None

    def get_musketeers(self):
        musketeers = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 'M':
                    musketeers.append((i, j))
        return musketeers

    def is_winner(self):
        pass

    def is_game_over(self):
        offsets = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        for musketeer in self.get_musketeers():
            for offset in offsets:
                if 0 <= musketeer[0] + offset[0] < 4 and 0 <= musketeer[1] + offset[1] < 4:
                    if self.board[musketeer[0] + offset[0]][musketeer[1] + offset[1]] != ' ':
                        return False
        return True

    def play_vs_comp(self):
        pass

    def play_vs_human(self):
        pass

    def play_vs_ai(self):
        pass


def three_musketeers(opp):
    game = ThreeMusketeers()
    print(game.is_game_over())


if __name__ == '_main_':
    print('' * 10 + '  THE THREE MUSKETEERS  ' + '' * 10)
    print('Main Menu')
    print('1. Play vs Computer')
    print('2. Play vs Human')
    print('3. Play vs AI')
    print('4. Exit')
    option = input('Choose your option: ')
    if option == '1':
        three_musketeers('C')
