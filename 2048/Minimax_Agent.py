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
        #print("esta actualizado 4.4")
        return self.policy(board)

    def minimax(self, board: GameBoard, deep: int, player: int):
        #Animación para que se vea lindo
        print(animation[int(self.idx/300) % len(animation)], end="\r")
        self.idx += 1

        # Caso Base returns (action, board, value)
        if deep >= 4:
            return (-1, board, self.heuristic_utility(board))
        if board.get_max_tile() >= 2048:
            return (-1, board, -1)
        if not board.get_available_moves():
            return (-1, board, 100000)

        #Casos no base
        actions = board.get_available_moves()
        random.shuffle(actions)
        action_nodes = []

        if player == 1:
            child_node = board.clone()
            for free_pos in child_node.get_available_cells():
                child_node.insert_tile(free_pos, 2)
                action_nodes.append(self.minimax(child_node, deep +1, 0))
            return max(action_nodes, key=lambda x: x[2])
        else:
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
        copy_board = board.clone()
        result_grid = np.square(copy_board.grid)
        return np.sum(result_grid)