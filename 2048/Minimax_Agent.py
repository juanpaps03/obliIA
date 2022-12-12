from Agent import Agent
from GameBoard import GameBoard
import numpy as np
import random

animation = [
    "[=     ]",
    "[ =    ]",
    "[  =   ]",
    "[   =  ]",
    "[    = ]",
    "[     =]",
    "[    = ]",
    "[   =  ]",
    "[  =   ]",
    "[ =    ]",
]


class MinimaxAgent(Agent):

    def policy(self, board: GameBoard):
        self.idx = 0
        act, _, _ = self.minimax(board, 0 , 0)
        return act

    def play(self, board: GameBoard):
        policy = self.policy(board)
        return policy

    def minimax(self, board: GameBoard, deep: int, player: int):
        #Animación para que se vea lindo
        print(animation[int(self.idx/300) % len(animation)], end="\r")
        self.idx += 1

        # Caso Base returns (action, board, value)
        if board.get_max_tile() >= 2048:
            return (-1, board, -10e10)
        if not board.get_available_moves():
            return (-1, board, 10e5)
        if deep == 5:
            return (-1, board, self.heuristic_utility(board))

        #Casos no base
        action_nodes = []

        if player == 1:
            child_node = board.clone()
            # Recorro solo los primeros 5 lugares libres ya que cuando hay muchos lugares libres
            # explorarlos todos no aporta valor y demora mucho
            available_cells = child_node.get_available_cells()[:5]
            random.shuffle(available_cells)
            for free_pos in available_cells:
                child_node.insert_tile(free_pos, 2)
                action_nodes.append(self.minimax(child_node, deep +1, 0))
            return max(action_nodes, key=lambda x: x[2])
        else:

            actions = board.get_available_moves()
            random.shuffle(actions)
            for action in actions:
                child_node = board.clone()
                child_node.move(action)
                action_nodes.append((action, board, self.minimax(child_node, deep +1, 1)[2]))
            return min(action_nodes, key=lambda x: x[2])


    def heuristic_smoothness(self, board: GameBoard) -> int:
        copy_board = board.clone()
        grid = np.sqrt(copy_board.grid)
        total = 0
        for i, fila in enumerate(grid[:-1]):
            for j, value in enumerate(fila):
                total = value + abs(value - grid[i+1, j])

        for i, fila in enumerate(grid):
            for j, value in enumerate(fila[:-1]):
                total = value + abs(value - grid[i, j+1])
        
        return (total ** 2) * -1
    

    def heuristic_total_board(self, board: GameBoard) -> int:
        copy_board = board.clone()
        grid = np.square(copy_board.grid)
        return np.sum(grid) * -1

    
    def heuristic_weight_board(self, board: GameBoard) -> int:
        WEIGHT_MATRIX = [
            [2048, 1024, 512, 256],
            [256, 128, 16, 2],
            [64, 16, 2, 1],
            [4, 2, 1, 1]
        ]
        result = 0
        for i, row in enumerate(board.grid):
            for j, val in enumerate(row):
                result += val * WEIGHT_MATRIX[i][j]

        return result * -1
    
    def heuristic_max_tile_position(self, board: GameBoard) -> int:
        max_tile = board.get_max_tile()
        if board.grid[0,0] == max_tile:
            return -10000
        return 2048

    def heuristic_utility(self, board: GameBoard) -> int:
        weight_board_h = self.heuristic_weight_board(board)
        smoothness_h = self.heuristic_smoothness(board)
        total_board_value_h = self.heuristic_total_board(board)
        tile_max_position_h = self.heuristic_max_tile_position(board)

        alpha = 2.8
        beta = 1.7
        gama = 1
        return (weight_board_h * alpha) + (smoothness_h * beta) + (total_board_value_h * gama) + tile_max_position_h

        

        

