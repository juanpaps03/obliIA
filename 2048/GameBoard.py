import numpy as np
from numba import jit

dirs = [UP, DOWN, LEFT, RIGHT] = range(4)


@jit
def merge(a):
    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2]:
            if a[i][j] == a[i][j + 1] and a[i][j] != 0:
                a[i][j] *= 2
                a[i][j + 1] = 0
    return a


@jit
def justify_left(a, out):
    for i in [0, 1, 2, 3]:
        c = 0
        for j in [0, 1, 2, 3]:
            if a[i][j] != 0:
                out[i][c] = a[i][j]
                c += 1
    return out


@jit
def get_available_from_zeros(a):
    uc, dc, lc, rc = False, False, False, False

    v_saw_0 = [False, False, False, False]
    v_saw_1 = [False, False, False, False]

    for i in [0, 1, 2, 3]:
        saw_0 = False
        saw_1 = False

        for j in [0, 1, 2, 3]:

            if a[i][j] == 0:
                saw_0 = True
                v_saw_0[j] = True

                if saw_1:
                    rc = True
                if v_saw_1[j]:
                    dc = True

            if a[i][j] > 0:
                saw_1 = True
                v_saw_1[j] = True

                if saw_0:
                    lc = True
                if v_saw_0[j]:
                    uc = True

    return [uc, dc, lc, rc]


class GameBoard:
    def __init__(self):
        self.grid = np.zeros((4, 4))  # , dtype=np.int_)
        self.__add_random_tile()
        self.__add_random_tile()

    def render(self)->None:
        """Imprime el tablero en consola"""
        for i in range(4):
            for j in range(4):
                print("%6d  " % self.grid[i][j], end="")
            print("")
        print("")

    def clone(self)->'GameBoard':
        """Me devuelve otro board igual"""
        board_clone = GameBoard()
        board_clone.grid = np.copy(self.grid)
        return board_clone

    def insert_tile(self, pos:tuple[int,int], value:int)->None:
        """Agrega una ficha en la posicion indicada (x,y), con el valor indicado"""
        self.grid[pos[0]][pos[1]] = value

    def get_available_cells(self)->list[tuple[int,int]]:
        """Devuelve todas las posiciones en las que se puede agregar una ficha"""
        cells = []
        for x in range(4):
            for y in range(4):
                if self.grid[x][y] == 0:
                    cells.append((x, y))
        return cells

    def get_max_tile(self)->int:
        """Devuelve cual es el valor de la ficha mas grande del tablero"""
        return np.amax(self.grid)

    def move(self, dir:int, get_avail_call=False):
        """
        Ejecuta una accion. Es decir, mueve todo el tablero en la direccion indicada,\n
        y junta las fichas que corresponda juntar
        """
        if get_avail_call:
            clone = self.clone()

        z1 = np.zeros((4, 4))  # , dtype=np.int_)
        z2 = np.zeros((4, 4))  # , dtype=np.int_)

        if dir == UP:
            self.grid = self.grid[:, ::-1].T
            self.grid = justify_left(self.grid, z1)
            self.grid = merge(self.grid)
            self.grid = justify_left(self.grid, z2)
            self.grid = self.grid.T[:, ::-1]
        if dir == DOWN:
            self.grid = self.grid.T[:, ::-1]
            self.grid = justify_left(self.grid, z1)
            self.grid = merge(self.grid)
            self.grid = justify_left(self.grid, z2)
            self.grid = self.grid[:, ::-1].T
        if dir == LEFT:
            self.grid = justify_left(self.grid, z1)
            self.grid = merge(self.grid)
            self.grid = justify_left(self.grid, z2)
        if dir == RIGHT:
            self.grid = self.grid[:, ::-1]
            self.grid = self.grid[::-1, :]
            self.grid = justify_left(self.grid, z1)
            self.grid = merge(self.grid)
            self.grid = justify_left(self.grid, z2)
            self.grid = self.grid[:, ::-1]
            self.grid = self.grid[::-1, :]

        if get_avail_call:
            return not (clone.grid == self.grid).all()
        else:
            return None

    def get_available_moves(self, dirs:list[int]=dirs)->list[int]:
        """
        Devuelve cuales movimientos se pueden hacer con el estado actual\n
        Por ejemplo :\n
            \t0   0   0   2\n
            \t0   0   0   4\n
            \t0   0   0   2\n
            \t0   0   0   4\n
            \tDevuelve solo izquierda\n
        """
        available_moves = []

        a1 = get_available_from_zeros(self.grid)

        for x in dirs:
            if not a1[x]:
                board_clone = self.clone()

                if board_clone.move(x, True):
                    available_moves.append(x)

            else:
                available_moves.append(x)

        return available_moves

    def play(self, dir:int):
        """
        Mueve el tablero en la posicion indicada, y agrega una ficha en una posicion al azar\n
        La posibilidad de que la ficha sea un:\n
            \t2 - 90%\n
            \t4 - 10%\n
        """
        self.move(dir)
        self.__add_random_tile()
        return len(self.get_available_moves()) == 0

    def __add_random_tile(self):
        if np.random.random_integers(0, 99) < 90:
            value = 2
        else:
            value = 4

        cells = self.get_available_cells()
        pos = cells[np.random.random_integers(
            0, len(cells) - 1)] if cells else None

        if pos is None:
            return None
        else:
            self.insert_tile(pos, value)
            return pos
