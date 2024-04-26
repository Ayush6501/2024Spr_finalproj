from ThreeM import ThreeMusketeers
from ThreeMGPU import ThreeMusketeersGPU
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


def three_musketeers(char, diff):
    game = ThreeMusketeers(char, diff)
    game.get_musketeers()
    player = True

    if char == 'M':
        while game.are_moves_available():
            game.print_board()
            moves = game.generate_valid_moves(player)
            if player:
                print('Following are the valid moves: ')
                for musk, move in moves.items():
                    print('Musketeer {}: {}'.format(musk, move))
                next_input_musk = int(input("Enter the number of the musketeer you would like to move: "))
                next_input_index = int(input("Enter the index (starting from 1) of the musketeer you want to move: "))
                game.make_move(game.musketeers_position[next_input_musk],
                               moves[next_input_musk][next_input_index - 1], next_input_musk,
                               True)
                print('Musketeer to {}'.format(moves[next_input_musk][next_input_index - 1]))
            else:
                # for space, move in moves.items():
                #     print('Space {}: {}'.format(space, move))
                board = copy.deepcopy(game.board)
                a, b = game.minimax(board, difficulty, False)
                print('AI moves: {} to {}'.format(b[0], b[1]))
                game.make_move(b[0], b[1], None, False)
            print()
            player = not player
    else:
        while game.are_moves_available():
            game.print_board()
            moves = game.generate_valid_moves(player)
            if player:
                board = copy.deepcopy(game.board)
                a, b = game.minimax(board, difficulty, True)
                print('AI moves: {} to {}'.format(b[1], b[0]))
                game.make_move(b[1], b[0], None, True)
            else:
                spaces = list(moves.keys())
                c = 1
                for space, move in moves.items():
                    print('Space {} {}: {}'.format(c, space, move))
                    c += 1
                space_index = int(input("Enter the space you want to conquer: "))
                print('Available Enemies: ' + str(moves[spaces[space_index-1]]))
                enemy_index = int(input("Enter the enemy index(starting with 1) you want to conquer with: "))
                print(spaces[space_index-1], moves[spaces[space_index-1]][enemy_index-1])
                game.make_move(moves[spaces[space_index-1]][enemy_index-1], spaces[space_index-1], None, False)
            print()
            player = not player

    if game.did_enemy_win():
        print("Cardinal Richelieu's Men Won!")
        if char == 'E':
            tprint('You Won!')
        else:
            tprint('You Lose!')
    else:
        print('The Three Musketeers won')
        if char == 'M':
            tprint('You Won!')
        else:
            tprint('You Lose!')
    return


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
    character = input('Choose your player: ')
    if character == '1':
        difficulty = select_difficulty()
        print("You are playing as the Three Musketeers!")
        three_musketeers('M', difficulty)
    if character == '2':
        difficulty = select_difficulty()
        print("You are playing as Cardinal Richelieu!")
        three_musketeers('E', difficulty)
