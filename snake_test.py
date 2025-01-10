import random
import sys

# Game board size
BOARD_SIZE = 10

# Snake initial position
SNAKE_START = (5, 5)

# Food initial position
FOOD_START = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))

# Possible directions
DIRECTIONS = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1)
}

# Print game board
def print_board(board):
    for row in board:
        print(" ".join(["#" if cell == 0 else "S" if cell == 1 else "F" for cell in row]))
    print()

# Initialize game board
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
board[FOOD_START[0]][FOOD_START[1]] = 2

# Initialize snake
snake = [SNAKE_START]
board[SNAKE_START[0]][SNAKE_START[1]] = 1

# Initialize game loop
while True:
    # Get user input
    direction = input("Enter direction (w/a/s/d): ")

    # Update snake position
    dx, dy = DIRECTIONS.get(direction, (0, 0))
    new_x, new_y = snake[0][0] + dx, snake[0][1] + dy

    # Check for wall collision
    if new_x < 0 or new_x >= BOARD_SIZE or new_y < 0 or new_y >= BOARD_SIZE:
        print("Game over!")
        sys.exit()

    # Check for self collision
    if (new_x, new_y) in snake:
        print("Game over!")
        sys.exit()

    # Check for food
    if board[new_x][new_y] == 2:
        # Grow snake
        snake.append((new_x, new_y))
        board[new_x][new_y] = 1
        # Move food to new position
        FOOD_START = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))
        board[FOOD_START[0]][FOOD_START[1]] = 2
    else:
        # Move snake
        snake.insert(0, (new_x, new_y))
        board[snake[0][0]][snake[0][1]] = 1
        # Remove tail
        board[snake[-1][0]][snake[-1][1]] = 0
        snake.pop()

    # Print game board
    print_board(board)