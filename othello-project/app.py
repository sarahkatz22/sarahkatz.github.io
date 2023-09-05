from flask import Flask, request, jsonify

app = Flask(__name__)

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
    app.run()

