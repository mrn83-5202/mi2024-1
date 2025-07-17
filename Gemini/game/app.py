from flask import Flask, render_template, request, jsonify
from game import TicTacToe
from computer_player import get_computer_move

app = Flask(__name__)

# We will store the game instance in memory.
# For a real multi-user application, you would use sessions or a database.
game = None

@app.route("/")
def index():
    """Serves the main game page."""
    return render_template("index.html")

@app.route("/start", methods=['POST'])
def start_game():
    """Starts a new game."""
    global game
    game = TicTacToe()
    return jsonify({
        'board': game.board,
        'status': "Your turn (X)"
    })

@app.route("/move", methods=['POST'])
def player_move():
    """Handles a player's move and the computer's subsequent move."""
    global game
    if game is None or game.current_winner or not game.has_empty_squares():
        return jsonify({'error': 'Game is not active. Please start a new game.'}), 400

    data = request.get_json()
    row, col = int(data['row']), int(data['col'])
    square = (row, col)

    # Player's move
    if not game.make_move(square, game.player_symbol):
        return jsonify({'error': 'Invalid move'}), 400

    # Check for player win or tie
    if game.current_winner:
        return jsonify({
            'board': game.board,
            'game_over': True,
            'status': 'Congratulations! You won!'
        })
    if not game.has_empty_squares():
        return jsonify({
            'board': game.board,
            'game_over': True,
            'status': "It's a tie!"
        })

    # Computer's move
    computer_square = get_computer_move(game)
    if computer_square:
        game.make_move(computer_square, game.computer_symbol)

    # Check for computer win or tie
    if game.current_winner:
        return jsonify({
            'board': game.board,
            'game_over': True,
            'status': 'The computer won! Better luck next time.'
        })
    if not game.has_empty_squares():
        return jsonify({
            'board': game.board,
            'game_over': True,
            'status': "It's a tie!"
        })

    return jsonify({
        'board': game.board,
        'game_over': False,
        'status': 'Your turn (X)'
    })

if __name__ == '__main__':
    app.run(debug=True)