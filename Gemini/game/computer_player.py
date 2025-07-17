import random

def get_computer_move(game):
    """
    Determines the best move for the computer.
    The strategy is:
    1. Check if the computer can win in the next move.
    2. Check if the player could win in the next move, and block them.
    3. Try to take the center square.
    4. Try to take one of the corner squares.
    5. Take any remaining middle side square.

    Args:
        game (TicTacToe): The current game instance.

    Returns:
        tuple: The (row, col) for the computer's move.
    """
    computer_symbol = game.computer_symbol
    player_symbol = game.player_symbol
    
    # 1. Check if the computer can win
    for move in game.get_available_moves():
        # Temporarily make the move
        game.board[move[0]][move[1]] = computer_symbol
        if game.check_winner(move, computer_symbol):
            game.board[move[0]][move[1]] = ' ' # Undo the move
            return move
        game.board[move[0]][move[1]] = ' ' # Undo the move

    # 2. Check if the player can win and block them
    for move in game.get_available_moves():
        # Temporarily make the move for the player
        game.board[move[0]][move[1]] = player_symbol
        if game.check_winner(move, player_symbol):
            game.board[move[0]][move[1]] = ' ' # Undo the move
            return move
        game.board[move[0]][move[1]] = ' ' # Undo the move

    # 3. Try to take the center
    if (1, 1) in game.get_available_moves():
        return (1, 1)

    # 4. Try to take a corner
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    available_corners = [move for move in game.get_available_moves() if move in corners]
    if available_corners:
        return random.choice(available_corners)

    # 5. Try to take a middle side
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    available_sides = [move for move in game.get_available_moves() if move in sides]
    if available_sides:
        return random.choice(available_sides)

    # This part should ideally not be reached if there are available moves
    # but serves as a fallback.
    available_moves = game.get_available_moves()
    if available_moves:
        return random.choice(available_moves)
    
    return None # Should not happen in a normal game flow
