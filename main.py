from ThreeM import ThreeMusketeers
import copy
from art import *


def select_difficulty():
    print('Select your difficulty: ')
    print('1 - Easy')
    print('2 - Medium')
    print('3 - Hard')
    while True:
        try:
            diff = int(input("Enter your difficulty: "))

            # Check if the input is 'yes'
            if isinstance(diff, int) and 1 <= diff <= 3:
                print("Difficulty Chosen - " + str(diff))
                break
            else:
                print("Invalid input. Please enter a number to continue.")

        except KeyboardInterrupt:
            print("\nProgram interrupted by the user.")
    return diff


def three_musketeers(opp):
    game = ThreeMusketeers(opp)
    player = True

    while game.are_moves_available():
        game.print_board()
        moves = game.generate_valid_moves(player)
        print('Following are the valid moves: ')
        if player:
            for musk, move in moves.items():
                print('Musketeer {}: {}'.format(musk, move))
            next_input_musk = int(input("Enter the number of the musketeer you would like to move: "))
            next_input_index = int(input("Enter the index (starting from 1) of the musketeer you want to move: "))
            game.move_musketeer('M', next_input_musk, next_input_index, moves)
        else:
            for space, move in moves.items():
                print('Space {}: {}'.format(space, move))
            board = copy.deepcopy(game.board)
            a, b = game.minimax(board, 3, False)
            print(a, b)
            game.move_enemy(b[1], b[0])

        player = not player
    if game.did_enemy_win():
        print("Cardinal Richelieu's Men Won!")
    else:
        print('The Three Musketeers won')


if __name__ == '__main__':
    tprint('THE  THREE  MUSKETEERS', font='medium')

    tprint("Rules", font="small")
    print('1. The musketeer player can move a musketeer to any orthogonally (non-diagonal) '
          'adjacent space occupied by an enemy')
    print('2. The enemy can move one enemy piece to any orthogonally adjacent empty space.')
    print('3. The musketeers win if on their turn they cannot move due to there being no enemy pieces '
          'adjacent to any musketeer and they are not all on the same row or column')
    print('4. The enemy wins if it can force the three musketeers to be all on the same row or column. ')
    print()
    print()

    tprint("Main Menu", font="small")
    print("1. Press 1 to play as d'Artagnan")
    print("2. Press 2 to play as Cardinal Richelieu")
    player = input('Choose your player: ')
    if player == '1':
        difficulty = select_difficulty()
        print("You are playing as the Three Musketeers")
        three_musketeers('M')
    if player == '2':
        if player == '1':
            difficulty = select_difficulty()
            print("You are playing as the Three Musketeers")
            three_musketeers('E')