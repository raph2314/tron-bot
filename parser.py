#!/usr/bin/env python3

import json
from math import sqrt, pow, fabs
import random

sample = {"0,0": "wall", "0,1": "wall", "0,2": "wall", "0,3": "wall", "0,4": "wall", "0,5": "wall", "0,6": "wall",
"0,7": "wall", "0,8": "wall", "0,9": "wall", "0,10": "wall", "0,11": "wall", "1,0": "wall", "1,1": "", "1,2":
"", "1,3": "", "1,4": "", "1,5": "", "1,6": "", "1,7": "", "1,8": "", "1,9": "", "1,10": "", "1,11": "wall", "2,0":
"wall", "2,1": "", "2,2": "", "2,3": "", "2,4": "", "2,5": "", "2,6": "", "2,7": "", "2,8": "", "2,9": "", "2,10":
"", "2,11": "wall", "3,0": "wall", "3,1": "", "3,2": "", "3,3": "", "3,4": "", "3,5": "", "3,6": "", "3,7": "",
"3,8": "", "3,9": "", "3,10": "", "3,11": "wall", "4,0": "wall", "4,1": "", "4,2": "", "4,3": "", "4,4": "", "4,5":
"", "4,6": "", "4,7": "", "4,8": "", "4,9": "", "4,10": "trail", "4,11": "wall", "5,0": "wall", "5,1": "", "5,2": "trail",
"5,3": "trail", "5,4": "trail", "5,5": "trail", "5,6": "trail", "5,7": "trail", "5,8": "trail", "5,9": "trail", "5,10":"123456", "5,11": "wall", "6,0": "wall", "6,1": "", "6,2": "", "6,3": "", "6,4": "", "6,5": "", "6,6":
"", "6,7": "", "6,8": "", "6,9": "", "6,10": "", "6,11": "wall", "7,0": "wall", "7,1":"123455", "7,2":
"trail", "7,3": "trail", "7,4": "trail", "7,5": "trail", "7,6": "trail", "7,7": "trail", "7,8": "trail", "7,9": "123456",
"7,10": "", "7,11": "wall", "8,0": "wall", "8,1": "", "8,2": "", "8,3": "", "8,4": "", "8,5": "", "8,6": "", "8,7":
"", "8,8": "", "8,9": "", "8,10": "", "8,11": "wall", "9,0": "wall", "9,1": "", "9,2": "", "9,3": "", "9,4": "",
"9,5": "", "9,6": "", "9,7": "", "9,8": "", "9,9": "", "9,10": "", "9,11": "wall", "10,0": "wall", "10,1": "",
"10,2": "", "10,3": "", "10,4": "", "10,5": "", "10,6": "", "10,7": "", "10,8": "", "10,9": "", "10,10": "",
"10,11": "wall", "11,0": "wall", "11,1": "wall", "11,2": "wall", "11,3": "wall", "11,4": "wall", "11,5":
"wall", "11,6": "wall", "11,7": "wall", "11,8": "wall", "11,9": "wall", "11,10": "wall", "11,11": "wall"}

DEFENSIVE = "defensive"
AGGRESSIVE = "aggressive"
BOXED = "boxed"
IDLE = "idle"
BOARD_SIZE = 11
current_state = BOXED
empty_boxed_spaces = 0
move_buffer = []
location = []
BOXED_WITH_ENEMY = True

# Change this to teamID later
TEAMID = "123456"
ENEMYID = None

class Game:
    def __init__(self):
        self.current_state = AGGRESSIVE
        self.empty_boxed_spaces = 0
        self.game_state_prev = []
        self.game_state_curr = None
        self.prev_move = None
        self.future_move = None
        self.boxed = False

        self.head_loc = None
        self.enemy_loc = None

    def parse_message(self, msg):
        # Save previous state for FSM algorithms' use
        self.game_state_prev.append(self.game_state_curr)

        # Make a 2d array containing all locations (0: go, 1: no go)
        msg = json.loads(msg)
        location = []
        for i in range(BOARD_SIZE + 1):
            location.append([])
            for j in range(BOARD_SIZE + 1):
                idx = str(i) + ',' + str(j)
                if (msg[idx] == 'wall') or (msg[idx] == 'trail'):
                    # Walls and trails are no go
                    location[i].append(1)
                elif msg[idx] == '':
                    # Empty space is go
                    location[i].append(0)
                elif msg[idx] == TEAMID:
                    # Case for our snake head (value=2)
                    location[i].append(2)
                else:
                    # Case for enemy snake head (value=3)
                    ENEMYID = msg[idx]
                    location[i].append(3)

        self.game_state_curr = location

    def finite_state_machine(self):
        boxed = True
        find_all_empty_boxed_spaces(self.game_state_curr[0], self.game_state_curr[1])
        if boxed:
            self.current_state = BOXED
        if self.current_state == AGGRESSIVE:
            return aggressive_action()
        elif self.current_state == DEFENSIVE:
            return defensive_action()
        elif self.current_state == BOXED:
            return boxed_action()
        else:
            return idle_action()

    # def idle_action():
        #return move

    def aggressive_action(self):
        # Computes the Euclidean distance between head and enemy and scales it by 10 to avoid floats
        head_x = self.head_loc[0]
        head_y = self.head_loc[1]
        enemy_x = self.enemy_loc[0]
        enemy_y = self.enemy_loc[1]
        dist_prev = sqrt(pow(fabs(head_x - enemy_x), 2) + pow(fabs(head_y - enemy_y), 2)) * 10

        # Get all possible moves and minimize euclidian distance
        possible_moves = self.get_possible_moves()
        new_dist = dist_prev
        new_move = None

        for move in possible_moves:
            if move == "UP":
                head_x -= 1
                temp_dist = sqrt(pow(fabs(head_x - enemy_x), 2) + pow(fabs(head_y - enemy_y), 2)) * 10

                if temp_dist == dist_prev:
                    new_move = "UP"

                if temp_dist < new_dist:
                    new_dist = temp_dist
                    new_move = "UP"

            elif move == "DOWN":
                head_x += 1
                temp_dist = sqrt(pow(fabs(head_x - enemy_x), 2) + pow(fabs(head_y - enemy_y), 2)) * 10

                if temp_dist == dist_prev:
                    new_move = "DOWN"
                if temp_dist < new_dist:
                    new_dist = temp_dist
                    new_move = "DOWN"

            elif move == "RIGHT":
                head_y += 1
                temp_dist = sqrt(pow(fabs(head_x - enemy_x), 2) + pow(fabs(head_y - enemy_y), 2)) * 10
                if temp_dist == dist_prev:
                    new_move = "RIGHT"
                if temp_dist < new_dist:
                    new_dist = temp_dist
                    new_move = "RIGHT"

            elif move == "LEFT":
                head_y -= 1
                temp_dist = sqrt(pow(fabs(head_x - enemy_x), 2) + pow(fabs(head_y - enemy_y), 2)) * 10

                if temp_dist == dist_prev:
                    new_move = "LEFT"

                if temp_dist < new_dist:
                    new_dist = temp_dist
                    new_move = "LEFT"


        print(new_move)
        return new_move



    # def defensive_action():
        #return move

    def boxed_actions(self):
        if (is_move_valid(self.prev_move)):
            self.future_move = self.prev_move
        elif (is_move_valid(rotate_right(self.prev_move))):
            self.future_move = rotate_right(self.prev_move)
        elif (is_move_valid(rotate_right(rotate_right(self.prev_move)))):
            self.future_move = rotate_right(rotate_right(self.prev_move))
        else:
            self.future_move = rotate_right(rotate_right(rotate_right(self.prev_move)))
        return 0

    def rotate_right(move):
        if (move == "RIGHT"):
            return "DOWN"
        elif (move == "DOWN"):
            return "LEFT"
        elif (move == "LEFT"):
            return "UP"
        else:
            return "RIGHT"

    def rotate_left(move):
        if (move == "RIGHT"):
            return "UP"
        elif (move == "UP"):
            return "LEFT"
        elif (move == "LEFT"):
            return "DOWN"
        else:
            return "RIGHT"

    def find_heads(self):
        for i in range(BOARD_SIZE + 1):
            for j in range(BOARD_SIZE + 1):
                if (self.game_state_curr[i][j] == 2):
                    self.head_loc = (i, j)
                elif (self.game_state_curr[i][j] == 3):
                    self.enemy_loc = (i, j)

    def get_possible_moves(self):
            possible_moves = []
            if self.is_move_valid("UP"):
                possible_moves.append("UP")

            if self.is_move_valid("DOWN"):
                possible_moves.append("DOWN")

            if self.is_move_valid("RIGHT"):
                possible_moves.append("RIGHT")

            if self.is_move_valid("LEFT"):
                possible_moves.append("LEFT")

            return possible_moves

    def is_move_valid(self, move):
        if (move == "DOWN"):
            if (self.game_state_curr[self.head_loc[0] + 1][self.head_loc[1]] != 0):
                return False

            return True
        elif (move == "UP"):
            if (self.game_state_curr[self.head_loc[0] - 1][self.head_loc[1]] != 0):
                return False
            return True
        elif (move == "RIGHT"):
            if (self.game_state_curr[self.head_loc[0]][self.head_loc[1] + 1] != 0):
                return False
            return True
        elif (move == "LEFT"):
            if (self.game_state_curr[self.head_loc[0]][self.head_loc[1] - 1] != 0):
                return False
            return True
        return False

    def idle_action(self):
        random_move = random.randint(1, 5)
        if random_move == 1:
            if not self.is_move_valid(self, "UP"):
                idle_action(self)
                return
            self.future_move = "UP"
        elif random_move == 2:
            if not self.is_move_valid(self, "DOWN"):
                idle_action(self)
                return
            self.future_move = "DOWN"
        elif random_move == 3:
            if not self.is_move_valid(self, "RIGHT"):
                idle_action(self)
                return
            self.future_move = "RIGHT"
        elif random_move == 4:
            if not self.is_move_valid(self, "LEFT"):
                idle_action(self)
                return
            self.future_move = "LEFT"
        return

    def find_all_empty_boxed_spaces(self, i, j):
        empty_boxed_spaces+=1
        print("EMPTY")
        if (adjacent_to_enemy(i, j)):
            self.boxed = True
        if (location[i+1][j] == 0):
            find_all_empty_boxed_spaces(i+1, j)

        if (location[i-1][j] == 0):
            find_all_empty_boxed_spaces(i-1, j)

        if (location[i][j+1] == 0):
            find_all_empty_boxed_spaces(i, j+1)

        if (location[i][j-1] == 0):
            find_all_empty_boxed_spaces(i, j-1)

        return

    def adjacent_to_enemy(i, j):
        if (location[i+1][j] == 3):
            return True

        if (location[i-1][j] == 3):
            return True

        if (location[i][j+1] == 3):
            return True

        if (location[i][j-1] == 3):
            return True

        return False





tron = Game()

# This should be invoked from client upon message receipt
sample = json.dumps(sample)
tron.parse_message(sample)

tron.find_heads()
print(tron.game_state_curr)
tron.aggressive_action()

boxed_action()
