from abc import ABC, abstractmethod
from GameBoard import GameBoard
import numpy as np

# MOVES
# LEFT = 0
# UP = 1
# RIGHT = 2
# DOWN = 3

# Posibility of adding a 2 tile 90%
# Posibility of adding a 4 tile 10%


class Agent(ABC):

    @abstractmethod
    def play(self, board: GameBoard)->int:
        # Si sienten que necesitan cambiar la firma se puede cambiar, asegurence de cambiarla en el main
        return 0

    @abstractmethod
    def heuristic_utility(self, board: GameBoard)->int:
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
        pass
