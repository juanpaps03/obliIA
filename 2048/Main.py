# %%
from datetime import datetime
from GameBoard import GameBoard
from Agent import Agent
from Minimax_Agent import MinimaxAgent
import numpy as np


# %%
def check_win(board: GameBoard):
    return board.get_max_tile() >= 2048

int_to_string = ['UP', 'DOWN', 'LEFT', 'RIGHT']

# %%
def run_game(debug: bool = False):
    agent: Agent = MinimaxAgent()
    board: GameBoard = GameBoard()
    
    done = False
    moves = 0
    if debug:
        #board.render()
        start = datetime.now()
    
    while not done:        
        action = agent.play(board)
        done = board.play(action)
        done = done or check_win(board)
        moves += 1

    if debug:
        #board.render()
        print(f"Max tile: {board.get_max_tile()}")
        # print('\nTotal time: {}'.format(datetime.now() - start))
        # print('\nTotal Moves: {}'.format(moves))
        if check_win(board):
            print("WON THE GAME!!!!!!!!")
        else:
            print("BOOOOOOOOOO!!!!!!!!!")
    return check_win(board)


# %% [markdown]
# ### Ejecucion del agente minimax con 10 juegos, heuristic_weight_board, poda a los 5 niveles del arbol y considerando 7 casillas libres randomicamente, tambien se hicieron cambios en la WEIGHT_MATRIX

# %%
# Run multiple games to get a winrate

winrate = 0
count = 0
games = 10
for i in range(games):
    won = run_game(True)
    count += 1
    winrate += 1 if won else 0
    #print(f"van {count} juegos, se ganaron {winrate} y se perdieron {count - winrate}")

print(f"El winrate obtenido con {count} ejecuciones es de: {(winrate*100)/games}")



