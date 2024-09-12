"""
Name of Program: Battleship Game

Description:
This is a text-based implementation of the classic Battleship game. The game allows two players to place ships on their 
respective boards and then take turns to fire at each other's ships. The objective is to sink all of the opponent's ships 
by correctly guessing their locations.

Inputs:
- Player 1 and Player 2 place their ships on a 10x10 grid.
- Players input positions to fire at the opponent's board.

Outputs:
- The game displays the current state of both players' boards.
- The game announces hits, misses, and whether a ship has been sunk.
- The game announces the winner when all ships of one player are sunk.

Sources:
- ChatGPT was used where marked in comments and has been further explained in the code

Author: Zach Alwin, Kristin Boeckmann, Lisa Phan, Nicholas Hausler, Vinayak Jha

Creation Date: 09/11/2024
"""

BOARD_SIZE = 10  # The size of the board, 10x10
MAX_SHIP = 5     # Maximum number of ships a player can place

A_CHAR = 65      # ASCII value of 'A'

# Row labels: 1-10
ROWS = [str(i) for i in range(1, BOARD_SIZE + 1)]  
# Column labels: A-J
COLS = [chr(i) for i in range(A_CHAR, BOARD_SIZE + A_CHAR)]  

EMPTY = '.'      # Symbol representing an empty cell
SHIP = 'S'       # Symbol representing a ship

# Utility function to display a board
def display(board):
    print("  " + " ".join(COLS))  # Print column labels
    for i, row in enumerate(board):
        print(ROWS[i] + " " + " ".join(row))  # Print each row with its row label

# Create an empty 10x10 board
def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Convert letter and number to board coordinates
def get_coordinates(pos):
    row = int(pos[1:]) - 1  # Convert row part of position to integer index (0-based)
    col = ord(pos[0].upper()) - A_CHAR  # Convert column letter to integer index (0-based)
    return row, col

# Place a ship on the board and return its positions
def place_ship(board, size, orientation, direction, start):
    row, col = get_coordinates(start)  # Get starting coordinates
    positions = []  # List to store the positions of the ship
    if orientation == 'H':  # Horizontal placement
        if direction == 'H':  # Right
            for i in range(size):
                board[row][col + i] = SHIP  # Place ship part
                positions.append((row, col + i))  # Add position to list
        elif direction == 'L':  # Left
            for i in range(size):
                board[row][col - i] = SHIP  # Place ship part
                positions.append((row, col - i))  # Add position to list
    else:  # Vertical placement
        if direction == 'D':  # Down
            for i in range(size):
                board[row + i][col] = SHIP  # Place ship part
                positions.append((row + i, col))  # Add position to list
        elif direction == 'U':  # Up
            for i in range(size):
                board[row - i][col] = SHIP  # Place ship part
                positions.append((row - i, col))  # Add position to list
    return positions  # Return the list of positions

# Check if position is valid for placing the ship
def is_valid_position(pos):
    if len(pos) < 2 or len(pos) > 3:
        return False  # Invalid position length
    if pos[0].upper() not in COLS:
        return False  # Invalid column letter
    try:
        row = int(pos[1:])  # Extract row number
        if row < 1 or row > BOARD_SIZE:
            return False  # Row number out of range
    except ValueError:
        return False  # Invalid row number
    finally:
        return True  # Valid position

# Check if placing ship is valid
def valid_ship_placement(board, size, orientation, direction, start):
    row, col = get_coordinates(start)  # Get starting coordinates
    if orientation == 'H':  # Horizontal placement
        if direction == 'H':  # Right
            if col + size > BOARD_SIZE:
                return False  # Ship goes off the board to the right
            return all(board[row][col + i] == EMPTY for i in range(size))  # Check if all positions are empty
        elif direction == 'L':  # Left
            if col - size + 1 < 0:
                return False  # Ship goes off the board to the left
            return all(board[row][col - i] == EMPTY for i in range(size))  # Check if all positions are empty
    else:  # Vertical placement
        if direction == 'D':  # Down
            if row + size > BOARD_SIZE:
                return False  # Ship goes off the board downwards
            return all(board[row + i][col] == EMPTY for i in range(size))  # Check if all positions are empty
        elif direction == 'U':  # Up
            if row - size + 1 < 0:
                return False  # Ship goes off the board upwards
            return all(board[row - i][col] == EMPTY for i in range(size))  # Check if all positions are empty

# Fire at a position on the opponent's board.
def fire(board, pos, ships):
    row, col = get_coordinates(pos)  # Get coordinates of the position
    # We used ChatGPT to help with marking ships as sunk. Here's how it works:
    # We check if (row, col) is in the list of positions for each ship.
    # If it is, we remove that position. If the ship's list of positions becomes empty, it means the ship is sunk.
    # We return "hit_and_sunk" with the size of the ship. If not sunk, we just return "hit".
    if board[row][col] == SHIP:
        board[row][col] = "X"  # Mark hit on the board
        for ship in ships:
            if (row, col) in ship['positions']:
                ship['positions'].remove((row, col))  # Remove hit position from ship's list
                if not ship['positions']:  # If no positions left, ship is sunk
                    return "hit_and_sunk", ship['size']
        return "hit", None  # Ship is hit but not sunk
    elif board[row][col] == EMPTY:
        board[row][col] = "O"  # Mark miss on the board
        return "miss", None  # Missed
    else:
        return "already", None  # Already fired at this position

# Check if all ships are sunk
def all_ships_sunk(ships):
    return all(not ship['positions'] for ship in ships)  # Return True if all ships have no positions left

# Ship configuration
def ship_sizes(num_ships):
    return list(range(1, num_ships + 1))  # Return a list of ship sizes from 1 to num_ships

def place_ships(board, ship_list):
    ships = []  # List to store placed ships
    for ship_size in ship_list:
        while True:
            print(f"\nPlacing ship of size {ship_size}")
            display(board)  # Display the board
            start = input("Enter start position (e.g., A1): ")  # Get start position
            orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()  # Get orientation
            direction = input("Enter direction (H for right, L for left, D for down, U for up): ").upper()  # Get direction
            
            if not is_valid_position(start) or orientation not in ['H', 'V'] or direction not in ['H', 'L', 'D', 'U']:
                print("Invalid input. Try again.")  # Invalid input
                continue
            if valid_ship_placement(board, ship_size, orientation, direction, start):
                ship_positions = place_ship(board, ship_size, orientation, direction, start)  # Place the ship if valid ship placement
                # Track ship's positions to check if it is sunk later
                ships.append({'size': ship_size, 'positions': ship_positions})
                break
            else:
                print("Invalid placement. Try again.")  # Ship placement invalid
    return ships  # Return the list of placed ships

def get_num_ships():
    while True:
        try:
            num_ships = int(input(f"Enter number of ships per player (1 to {MAX_SHIP}): "))  # Get number of ships
            if 1 <= num_ships <= MAX_SHIP:
                return num_ships  # Valid number of ships
            else:
                print(f"Please enter a number between 1 and {MAX_SHIP}.")  # Out of range
        except ValueError:
            print("Invalid input. Please enter a valid number.")  # Invalid input

def battleship_game():
    # Initialize player boards
    player1_board = create_board()  # Board for Player 1
    player2_board = create_board()  # Board for Player 2

    # Get number of ships from user
    num_ships = get_num_ships()

    # Ship sizes based on number of ships
    player1_ships = ship_sizes(num_ships)  # Ship sizes for Player 1
    player2_ships = ship_sizes(num_ships)  # Ship sizes for Player 2

    # Place ships for Player 1 and Player 2
    print("Player 1, place your ships.")
    player1_ships = place_ships(player1_board, player1_ships)  # Place Player 1's ships
    print("Player 2, place your ships.")
    player2_ships = place_ships(player2_board, player2_ships)  # Place Player 2's ships

    # Game loop
    while True:
        # Player 1's turn
        print("Player 1's turn!")
        display(player2_board)  # Show Player 2's board
        pos = input("Enter position to fire at Player 2's board (e.g., A1): ")  # Get fire position
        result, size = fire(player2_board, pos, player2_ships)  # Fire at Player 2's board
        if result == "hit_and_sunk":
            print(f"Hit and sunk a ship of size {size}!")
        elif result == "hit":
            print("Hit!")
        elif result == "miss":
            print("Miss!")
        elif result == "already":
            print("You already fired at this position. Try again.")
            continue

        # Check if Player 2's ships are all sunk
        if all_ships_sunk(player2_ships):
            print("Player 1 wins!")
            break  # End the game

        # Player 2's turn
        print("Player 2's turn!")
        display(player1_board)  # Show Player 1's board
        pos = input("Enter position to fire at Player 1's board (e.g., A1): ")  # Get fire position
        result, size = fire(player1_board, pos, player1_ships)  # Fire at Player 1's board
        if result == "hit_and_sunk":
            print(f"Hit and sunk a ship of size {size}!")
        elif result == "hit":
            print("Hit!")
        elif result == "miss":
            print("Miss!")
        elif result == "already":
            print("You already fired at this position. Try again.")
            continue

        # Check if Player 1's ships are all sunk
        if all_ships_sunk(player1_ships):
            print("Player 2 wins!")
            break  # End the game

battleship_game()  # Start the game
