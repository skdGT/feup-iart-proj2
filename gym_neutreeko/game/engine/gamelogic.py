# Lógica do Jogo: https://github.com/towzeur/gym-abalone/blob/master/gym_abalone/game/engine/gamelogic.py
import numpy as np
from typing import Tuple, List, Union

import numpy.char


class NeutreekoGame:
    # Actions
    UP = (-1, 0)
    DOWN = (+1, 0)
    LEFT = (0, -1)
    RIGHT = (0, +1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, +1)
    DOWN_LEFT = (+1, -1)
    DOWN_RIGHT = (+1, +1)

    # ACTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

    ACTIONS_DICT = {'UP': (-1, 0),
               'DOWN': (+1, 0),
               'LEFT': (0, -1),
               'RIGHT': (0, +1),
               'UP_LEFT': (-1, -1),
               'UP_RIGHT': (-1, +1),
               'DOWN_LEFT': (+1, -1),
               'DOWN_RIGHT': (+1, +1)
               }

    # Players
    BLACK = 2
    WHITE = 1

    BOARD_SIZE = 5

    def __init__(self):
        self.board = None
        self.current_player = None
        self.game_over = None
        self.turns_count = None

    def reset(self):
        self.board = self.new_board()
        self.current_player = self.BLACK
        self.game_over = False
        self.turns_count = 0

    @staticmethod
    def new_board():
        """
        returns a fresh starting board, each element is a numpy.int8 (-128, 127)

        :return: numpy.array
        """
        return np.array([[0, 1, 0, 1, 0],
                         [0, 0, 2, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 2, 0, 2, 0]], dtype=np.int8)

    def value_in_board(self, position: Tuple[int, int]) -> int:
        """
        Returns the value in a position of the board

        :param position: Tuple with 2 ints representing the coordinates of a cell
        :return: The int value
        """
        return self.board[position[0], position[1]]

    def free_cell(self, coords: Tuple[int, int]) -> bool:
        """
        Checks if a cell is within bounds of the board and is free (value is 0)

        :param coords: Tuple with 2 ints representing the coordinates of a cell
        :return: True if the cell equals 0 and is within bounds
        """
        if (coords[0] < 0) | (coords[0] >= self.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= self.BOARD_SIZE):
            return False
        value = self.board[coords[0]][coords[1]]
        return value == 0

    def check_direction(self, coords: Tuple[int, int], direction: str) -> Union[None, Tuple[str, tuple]]:
        """
        Returns the resulting position given a starting position and a direction.
        If the direction is not valid, returns None

        :param coords: Coordinates of intial point
        :param direction: String representation of the direction to take
        :return: None if direction is not valid OR tuple with new coords of resulting positions
        """
        action_coords = self.ACTIONS_DICT[direction]
        attempt_coords = tuple(np.add(coords, action_coords))
        free_cell = self.free_cell(attempt_coords)
        if not free_cell:
            return None
        # apply direction until it reaches EOB (end of board) or another piece
        while free_cell:
            new_coords = attempt_coords
            attempt_coords = tuple(np.add(new_coords, action_coords))
            free_cell = self.free_cell(attempt_coords)
        return new_coords

    def available_directions(self, coords: Tuple[int, int]) -> List[Tuple[str, tuple]]:
        """
        For some starting coords, returns a list of pairs directions-finishing_coords
        FIXME: untested inside for loop, need to check if "check_direction" is working as intended
        """
        dirs = []
        for action_name in self.ACTIONS_DICT.keys():
            result = self.check_direction(coords, action_name)
            if result:
                dirs.append(result)
        return dirs

    def get_possible_moves(self, player: int, only_valid: bool = False) -> List[tuple]:
        """
        Return all the possible moves for a given player with the current board

        :param player: Integer representing the player
        :param only_valid: TODO Boolean to be used in the future
        :return: A list of tuples with the starting position and a direction
        """
        if only_valid:
            raise Exception("Not yet implemented")

        possible_moves = []

        result = np.where(self.board == player)
        list_of_coordinates = list(zip(result[0], result[1]))
        for pos in list_of_coordinates:
            for direction in self.ACTIONS_DICT.keys():
                possible_moves.append((pos, direction))

        return possible_moves

    def OLD_get_possible_moves(self, player: int) -> list:
        """
        Este método já dá as moves válidos. Pode ser usado mais tarde
        Será usado no método acima

        :param player: Valor inteiro do jogador que vai jogar
        :return:
        """
        # Encontra peças do player
        result = np.where(self.board == player)
        listOfCoordinates = list(zip(result[0], result[1]))
        # Vê quais as direções válidas para essa peça (função à parte para fazer)
        possible_moves = []
        for coords in listOfCoordinates:
            dirs = self.available_directions(coords)
            possible_moves.append((coords, dirs))
        return possible_moves

    def action_handler(self, pos, dir):
        """
        After the agent chooses a move, it needs to be checked to see if it's valid
        If it is valid, returns new position

        :param pos: The position of the piece that will be moved
        :param dir: The direction that the piece will be moved to
        :return:
        """

        print("IN ACTION HANDLER")
        player = self.value_in_board(pos)  # Nem sei se é preciso isso
        result = self.check_direction(pos, dir)
        print(result)
        pass