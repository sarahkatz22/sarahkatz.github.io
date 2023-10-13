# import os
# import sys
# project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(project_dir)

# from flask import Flask, request, jsonify
# from othello_project.gui.gui import GUI_it
# from othello_project.gui.reversi import Reversi, ReversiPiece

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
# cors = CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Your GUI code should be imported here (if needed)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message_from_client')
def handle_client_message(message):
    # Handle messages from the client (e.g., user interactions)
    # You can send messages back to the client as needed
    socketio.emit('message_from_server', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

