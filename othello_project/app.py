import os
import sys
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)

from flask import Flask, request, jsonify
from othello_project.gui.gui import GUI_it
from othello_project.gui.reversi import Reversi, ReversiPiece

app = Flask(__name__)
game = Reversi(side=8, players=2, othello=True)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/api/start_game', methods=['POST'])
def start_game(): 

    return jsonify({'message': 'Game started'})

@app.route('/api/make_move', methods=['POST'])
def make_move():
    # Implement logic to process player moves
    # Return game state or other relevant data as a JSON response
    return jsonify({'message': 'Move made'})

if __name__ == '__main__':
    gui_it = GUI_it(game=game)  # Initialize the GUI
    app.run()

