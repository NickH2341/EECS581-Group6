import random

BOARD_SIZE = 10
MAX_SHIP = 5

A_CHAR = 65

ROWS = [str(i) for i in range(1, BOARD_SIZE + 1)]  # Row labels: 1-10
COLS = [chr(i) for i in range(A_CHAR, BOARD_SIZE + A_CHAR)]  # Column labels: A-J

EMPTY = '.'
SHIP = 'S'

# Utility function to display a board
def display(board):
    print("  " + " ".join(COLS))
    for i, row in enumerate(board):
        print(ROWS[i] + " " + " ".join(row))

# Create an empty 10x10 board
def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Convert letter and number to board coordinates
def get_coordinates(pos):
    row = int(pos[1:]) - 1
    col = ord(pos[0].upper()) - A_CHAR
    return row, col

# Place a ship on the board
def place_ship(board, size, orientation, direction, start):
    row, col = get_coordinates(start)
    if orientation == 'H':
        if direction == 'H':
            for i in range(size):
                board[row][col + i] = SHIP
        elif direction == 'L':
            for i in range(size):
                board[row][col - i] = SHIP
    else:
        if direction == 'D':
            for i in range(size):
                board[row + i][col] = SHIP
        elif direction == 'U':
            for i in range(size):
                board[row - i][col] = SHIP

# Check if position is valid for placing the ship
def is_valid_position(pos):
    if len(pos) < 2 or len(pos) > 3:
        return False
    if pos[0].upper() not in COLS:
        return False
    try:
        row = int(pos[1:])
        if row < 1 or row > BOARD_SIZE:
            return False
    except ValueError:
        return False
    finally:
        return True

# Check if placing ship is valid
def valid_ship_placement(board, size, orientation, direction, start):
    row, col = get_coordinates(start)
    if orientation == 'H':
        if direction == 'H':
            if col + size > BOARD_SIZE:
                return False  # Ship goes off the board to the right
            return all(board[row][col + i] == EMPTY for i in range(size))
        elif direction == 'L':
            if col - size + 1 < 0:
                return False  # Ship goes off the board to the left
            return all(board[row][col - i] == EMPTY for i in range(size))
    else:
        if direction == 'D':
            if row + size > BOARD_SIZE:
                return False  # Ship goes off the board downwards
            return all(board[row + i][col] == EMPTY for i in range(size))
        elif direction == 'U':
            if row - size + 1 < 0:
                return False  # Ship goes off the board upwards
            return all(board[row - i][col] == EMPTY for i in range(size))

# Fire at opponent's board
def fire(board, pos):
    row, col = get_coordinates(pos)
    if board[row][col] == SHIP:
        board[row][col] = "X"  # Hit
        return True
    elif board[row][col] == EMPTY:
        board[row][col] = "O"  # Miss
        return False
    return False  # Already fired at this position

# Check if all ships are sunk
def all_ships_sunk(board):
    for row in board:
        if SHIP in row:
            return False
    return True

# Ship configuration
def ship_sizes(num_ships):
    return list(range(1, num_ships + 1))

def place_ships(board, ship_list):
    for ship in ship_list:
        while True:
            print(f"Placing ship of size {ship}")
            display(board)
            start = input("Enter start position (e.g., A1): ")
            orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
            direction = input("Enter direction (H for right, L for left, D for down, U for up): ").upper()
            
            if not is_valid_position(start) or orientation not in ['H', 'V'] or direction not in ['H', 'L', 'D', 'U']:
                print("Invalid input. Try again.")
                continue
            if valid_ship_placement(board, ship, orientation, direction, start):
                place_ship(board, ship, orientation, direction, start)
                break
            else:
                print("Invalid placement. Try again.")

def get_num_ships():
    while True:
        try:
            num_ships = int(input(f"Enter number of ships per player (1 to {MAX_SHIP}): "))
            if 1 <= num_ships <= MAX_SHIP:
                return num_ships
            else:
                print(f"Please enter a number between 1 and {MAX_SHIP}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def battleship_game():
    # Initialize player boards
    player1_board = create_board()
    player2_board = create_board()

    # Initialize player tracking boards (for hits/misses)
    player1_view = create_board()
    player2_view = create_board()

    # Ship placement
    print("Welcome to Battleship!")

    # Get the number of ships
    num_ships = get_num_ships()

    ship_list = ship_sizes(num_ships)

    # Player 1's turn
    print("\nPlayer 1, place your ships.")
    place_ships(player1_board, ship_list)

    # Player 2's turn
    print("\nPlayer 2, place your ships.")
    place_ships(player2_board, ship_list)

    player_turn = 1
    while True:
        if player_turn == 1:
            print("\nPlayer 1's turn!")
            print("Your board:")
            display(player1_board)  # Show Player 1's board with their ships
            print("Opponent's board:")
            display(player1_view)  # Show Player 1's view of Player 2's board
            pos = input("Enter position to fire (e.g., A1): ")
            if fire(player2_board, pos):
                print("Hit!")
                player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
            else:
                print("Miss!")
                player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O"
            if all_ships_sunk(player2_board):
                print("Player 1 wins! All ships sunk.")
                break
            player_turn = 2
        else:
            print("\nPlayer 2's turn!")
            print("Your board:")
            display(player2_board)  # Show Player 2's board with their ships
            print("Opponent's board:")
            display(player2_view)  # Show Player 2's view of Player 1's board
            pos = input("Enter position to fire (e.g., A1): ")
            if fire(player1_board, pos):
                print("Hit!")
                player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
            else:
                print("Miss!")
                player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O"
            if all_ships_sunk(player1_board):
                print("Player 2 wins! All ships sunk.")
                break
            player_turn = 1

battleship_game()
