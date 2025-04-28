import tkinter as tk
import copy
import random
from collections import deque

ROWS = 4
COLS = 4
EMPTY_TILE = ROWS * COLS

MOVE_UP = (-1, 0)
MOVE_DOWN = (1, 0)
MOVE_LEFT = (0, -1)
MOVE_RIGHT = (0, 1)


def generate_initial_state():
    initial_state = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, None]
    ]

    for _ in range(100):
        empty_row, empty_col = find_empty_tile(initial_state)
        possible_moves = get_possible_moves(empty_row, empty_col)
        move_row, move_col = possible_moves.pop(random.randint(0, len(possible_moves) - 1))
        initial_state[empty_row][empty_col], initial_state[move_row][move_col] = \
            initial_state[move_row][move_col], initial_state[empty_row][empty_col]

    return initial_state


def find_empty_tile(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] is None:
                return i, j


def get_possible_moves(empty_row, empty_col):
    possible_moves = []
    if empty_row > 0:
        possible_moves.append((empty_row - 1, empty_col))  # Move up
    if empty_row < 3:
        possible_moves.append((empty_row + 1, empty_col))  # Move down
    if empty_col > 0:
        possible_moves.append((empty_row, empty_col - 1))  # Move left
    if empty_col < 3:
        possible_moves.append((empty_row, empty_col + 1))  # Move right
    return possible_moves


def is_solved(state):
    k = 1
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] != k:
                return False
            k = k + 1
    return True


def manhattan_distance(state):
    distance = 0
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] is not None:
                goal_row = (state[i][j] - 1) // COLS
                goal_col = (state[i][j] - 1) % COLS
                distance = distance + abs(i - goal_row) + abs(j - goal_col)
    return distance


def generate_successor_states(state):
    successor_states = []
    empty_row, empty_col = find_empty_tile(state)

    for dr, dc in [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]:
        new_row, new_col = empty_row + dr, empty_col + dc
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            new_state = copy.deepcopy(state)
            new_state[empty_row][empty_col], new_state[new_row][new_col] = \
                new_state[new_row][new_col], new_state[empty_row][empty_col]
            successor_states.append(new_state)

    return successor_states


def update_puzzle_board(puzzle_board, state):
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] is None:
                puzzle_board[i][j].config(text="", state=tk.DISABLED)  # Empty tile
            else:
                puzzle_board[i][j].config(text=str(state[i][j]), state=tk.NORMAL)  # Numbered tile


def handle_tile_click(row, col):
    global current_state  # Current State of Puzzle
    global puzzle_board   
    
    # Find empty tile position
    empty_row, empty_col = find_empty_tile(current_state)
    
    # Check if the clicked tile is adjacent to the empty tile
    if (row == empty_row and abs(col - empty_col) == 1) or (col == empty_col and abs(row - empty_row) == 1):
        
        # Swapping Clicked tile with Empty tile
        current_state[empty_row][empty_col], current_state[row][col] = current_state[row][col], current_state[empty_row][empty_col]
        
        # Update puzzle board display
        update_puzzle_board(puzzle_board, current_state)
        
        # Check if puzzle is solved
        if is_solved(current_state):
            print("Congratulations! Puzzle solved!")
    else:
        print("Invalid move. Please select an adjacent tile to the empty tile.")


root = tk.Tk()
root.title("15 Puzzle Game")

puzzle_board = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        tile = tk.Button(root, width=10, height=5)
        tile.grid(row=i, column=j)
        row.append(tile)
    puzzle_board.append(row)

current_state = generate_initial_state()
update_puzzle_board(puzzle_board, current_state)

for i in range(ROWS):
    for j in range(COLS):
        puzzle_board[i][j].config(command=lambda row=i, col=j: handle_tile_click(row, col))

root.mainloop()