
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import time
from ai_agent import Heuristic, MiniMax, MiniMaxAlphaBeta, ExpectMinimax
from board import Board

app = Flask(__name__)
CORS(app)


main_board = Board()


VALID_ALGORITHMS = ["minimax", "minimax_alpha_beta", "expect_minimax"]
VALID_PLAYERS = [1, 2]

def start_game(board, depth, ai_player, opp_player):

    heuristic = Heuristic(ai_player, opp_player)
    minimax = MiniMax(board, depth, heuristic, ai_player, opp_player)
    minimax_alpha_beta = MiniMaxAlphaBeta(board, depth, heuristic, ai_player, opp_player)
    expect_minimax = ExpectMinimax(board, depth, heuristic, ai_player, opp_player)
    return heuristic, minimax, minimax_alpha_beta, expect_minimax

def get_board_data():

    return {
        "board": main_board.grid.tolist(),
        "valid_moves": main_board.get_valid_cols(),
        "is_terminal": main_board.isterminal(),
        "move_count": main_board.move_count
    }

@app.route("/")
def home():

    return render_template("index.html")

@app.route('/board', methods=['GET'])
def get_board():

    try:
        return jsonify(get_board_data()), 200
    except Exception as e:
        return jsonify({"error": "Failed to get board state"}), 500

@app.route('/reset', methods=['POST'])
def reset():

    global main_board
    try:
        main_board = Board()
        return jsonify(get_board_data()), 200
    except Exception as e:
        return jsonify({"error": "Failed to reset board"}), 500

# related to the player
@app.route('/move', methods=['POST'])
def make_move():

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body required"}), 400

        if 'col' not in data or 'player' not in data:
            return jsonify({"error": "Missing 'col' or 'player'"}), 400

        col = data['col']
        player = data['player']


        if not isinstance(col, int) or col < 0 or col >= 7:
            return jsonify({"error": "Column must be 0-6"}), 400

        if player not in VALID_PLAYERS:
            return jsonify({"error": f"Player must be {VALID_PLAYERS}"}), 400

        if not main_board.isvalidmove(col):
            return jsonify({
                "error": "Invalid move - column full",
                "valid_moves": main_board.get_valid_cols()
            }), 400


        main_board.makemove(col, player)

        return jsonify(get_board_data()), 200

    except Exception as e:
        return jsonify({"error": "Failed to make move"}), 500

# related to ai
@app.route('/play', methods=['POST'])
def play():

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body required"}), 400


        algorithm = data.get('algorithm', 'minimax_alpha_beta')
        depth = data.get('depth', 5)
        ai_player = data.get('ai_player', 2)
        opp_player = data.get('opp_player', 1)
        auto_move = data.get('auto_move', True)


        if algorithm not in VALID_ALGORITHMS:
            return jsonify({
                "error": f"Invalid algorithm. Use: {', '.join(VALID_ALGORITHMS)}"
            }), 400


        try:
            depth = int(depth)
            if depth < 1 or depth > 10:
                return jsonify({"error": "Depth must be between 1 and 10"}), 400
        except (TypeError, ValueError):
            return jsonify({"error": "Depth must be an integer"}), 400


        if ai_player not in VALID_PLAYERS or opp_player not in VALID_PLAYERS:
            return jsonify({"error": f"Players must be {VALID_PLAYERS}"}), 400

        if ai_player == opp_player:
            return jsonify({"error": "Players must be different"}), 400

        if main_board.isterminal():
            return jsonify({
                "error": "Game is over",
                **get_board_data()
            }), 400


        valid_moves = main_board.get_valid_cols()
        if not valid_moves:
            return jsonify({"error": "No valid moves available"}), 400


        start_time = time.time()
        _, minimax, minimax_alpha_beta, expect_minimax = start_game(
            main_board, depth, ai_player, opp_player
        )

        alg_map = {
            "minimax": minimax,
            "minimax_alpha_beta": minimax_alpha_beta,
            "expect_minimax": expect_minimax,
        }

        algo_instance = alg_map[algorithm]
        best_col = algo_instance.get_best_move()
        calculation_time = time.time() - start_time


        if best_col is None or not main_board.isvalidmove(best_col):
            return jsonify({"error": "AI failed to find valid move"}), 500

        if auto_move:
            main_board.makemove(best_col, ai_player)


        response = get_board_data()
        response.update({
            "best_col": best_col,
            "calculation_time": round(calculation_time, 3),
            "algorithm": algorithm,
            "auto_move": auto_move
        })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
