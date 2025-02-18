from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# A simple function to initialize the board
def initialize_board():
    return [['' for _ in range(3)] for _ in range(3)]

# Global game state
game_state = {
    'board': initialize_board(),
    'turn': 'X',  # X always starts
    'winner': None
}

# Route to render the game board
@app.route('/')
def index():
    return render_template('index.html', board=game_state['board'], winner=game_state['winner'])

# Route to handle player moves
@app.route('/move/<int:row>/<int:col>', methods=['POST'])
def make_move(row, col):
    if game_state['board'][row][col] == '' and game_state['winner'] is None:
        game_state['board'][row][col] = game_state['turn']
        
        # Check for winner
        if check_winner(game_state['turn']):
            game_state['winner'] = game_state['turn']
        else:
            # Switch turn
            game_state['turn'] = 'O' if game_state['turn'] == 'X' else 'X'
        
    return jsonify({'board': game_state['board'], 'winner': game_state['winner'], 'turn': game_state['turn']})

# Function to check for a winner
def check_winner(player):
    # Check rows and columns for a win
    for i in range(3):
        if all(game_state['board'][i][j] == player for j in range(3)) or \
           all(game_state['board'][j][i] == player for j in range(3)):
            return True
    
    # Check diagonals
    if game_state['board'][0][0] == player and game_state['board'][1][1] == player and game_state['board'][2][2] == player:
        return True
    if game_state['board'][0][2] == player and game_state['board'][1][1] == player and game_state['board'][2][0] == player:
        return True
    
    return False
@app.route('/reset', methods=['POST'])
def reset_game():
    game_state['board'] = initialize_board()
    game_state['turn'] = 'X'
    game_state['winner'] = None
    return jsonify({'board': game_state['board']})
if __name__ == '__main__':
    app.run(debug=True)
