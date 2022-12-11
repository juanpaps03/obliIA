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
            return (-1, board, -100000)
        if not board.get_available_moves():
            return (-1, board, 100000)
        if deep == 5:
            return (-1, board, self.heuristic_weight_board(board))

        #Casos no base
        action_nodes = []

        if player == 1:
            child_node = board.clone()
            # Recorro solo los primeros 5 lugares libres ya que cuando hay muchos lugares libres
            # explorarlos todos no aporta valor y demora mucho
            available_cells = child_node.get_available_cells()[:5]
            random.shuffle(available_cells)
            for free_pos in available_cells:
                child_node.insert_tile(free_pos, 4)
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


    def heuristic_utility(self, board: GameBoard) -> int:
        """
        Algunas heurisitcas posibles son:\n
            - Calcular el \"smoothness\" del tablero. Esto es porque cuanto mas \"smooth\" el tablero, mas facil es juntar fichas. Para ello debemos:
                - Aplicar la raiz cuadrada al tablero
                - Sumar la diferencia entre cada casilla y la de abajo
                - Sumar la diferencia entre cada casilla y la de la derecha
                - Elevar este resultado a un smoothness_weight a determinar
                - Multiplicar por -1
            - Calcular el valor del tablero. Esto es porque cuanto mas fichas grandes tengo, mas cerca de ganar estoy. Para ello debemos:
                - Elevar el tablero al cuadrado
                - Sumar todos los valores que se encuentran en el tablero
            - Calcular la cantidad de espacios vacios. Esto es porque cuanto mas espacios vacios tengo, menos chance de tener un mal estado. Para ello debemos:
                - Obtener la cantidad de celdas vacias
                - Multiplicar por un empty_weight (recomendable en el orden de las decenas de miles)
        """
        smoothness_weight = 0.7
        copy_board = board.clone()
        grid = np.sqrt(copy_board.grid)
        total = 0
        for i, fila in enumerate(grid[:-1]):
            for j, value in enumerate(fila):
                total = value + abs(value - grid[i+1, j])

        for i, fila in enumerate(grid):
            for j, value in enumerate(fila[:-1]):
                total = value + abs(value - grid[i, j+1])
        
        return (total ** smoothness_weight) * -1

    
    def heuristic_weight_board(self, board: GameBoard) -> int:
        WEIGHT_MATRIX = [
            [2048, 1024, 64, 32],
            [512, 128, 16, 2],
            [256, 8, 2, 1],
            [4, 2, 1, 1]
        ]
        WEIGHT_MATRIX = [
            [65536,32768,16384,8192],
            [512,2048,1024,1024],
            [256,128,64,32],
            [2,4,8,16]]
        result = 0
        for i, row in enumerate(board.grid):
            for j, val in enumerate(row):
                result += val * WEIGHT_MATRIX[i][j]

        return result * -1

        

        

