from datetime import datetime
from GameBoard import GameBoard
from Agent import Agent
from Random_Agent import RandomAgent

def check_win(board: GameBoard):
    return board.get_max_tile() >= 2048


int_to_string = ['UP', 'DOWN', 'LEFT', 'RIGHT']

if __name__ == '__main__':
    agent: Agent
    board: GameBoard
    agent = RandomAgent()
    board = GameBoard()
    done = False
    moves = 0
    board.render()
    start = datetime.now()
    while not done:
        action = agent.play(board)
        print('Next Action: "{}"'.format(
            int_to_string[action]), ',   Move: {}'.format(moves))
        done = board.play(action)
        done = done or check_win(board)
        board.render()
        moves += 1

    print('\nTotal time: {}'.format(datetime.now() - start))
    print('\nTotal Moves: {}'.format(moves))
    if check_win(board):
        print("WON THE GAME!!!!!!!!")
    else:
        print("BOOOOOOOOOO!!!!!!!!!")
