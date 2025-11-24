from flask import Flask, jsonify, request
from flask_cors import CORS
import board
import ai_agent

app = Flask(__name__)
CORS(app) 

game_board = None
ai_brain = None

@app.route('/start', methods=['POST'])
def start_game():
    global game_board, ai_brain
    data = request.json
    
    game_board = board.Board()
    algo_type = data.get('algo', 1) 
    k_depth = data.get('depth', 3)
    
    heuristic = ai_agent.Heuristic(ai_player=2, opp_player=1)
    if algo_type == 1:
        ai_brain = ai_agent.MiniMax(game_board, k_depth, heuristic, 2, 1)
    elif algo_type == 2:
        ai_brain = ai_agent.MiniMaxAlphaBeta(game_board, k_depth, heuristic, 2, 1)
    elif algo_type == 3:
        ai_brain = ai_agent.ExpectMinimax(game_board, k_depth, heuristic, 2, 1)
    
    return jsonify({"message": "Game Started", "grid": game_board.grid.tolist()})

@app.route('/move', methods=['POST'])
def make_move():
    global game_board, ai_brain
    
    if not game_board:
        return jsonify({"error": "Game not started"}), 400

    data = request.json
    col = data.get('col')
    
    if game_board.isvalidmove(col):
        game_board.makemove(col, 1)
        human_score = game_board.coount_connected_four(1) 
        ai_score = game_board.coount_connected_four(2)   
        if game_board.isterminal():
             diff = game_board.get_difference(1, 2)
             return jsonify({
                 "grid": game_board.grid.tolist(), 
                 "game_over": True, 
                 "winner": "Human" if diff > 0 else "Draw" ,
                 "human_score": human_score,
                 "ai_score": ai_score        
             })
    else:
        return jsonify({"error": "Invalid Move"}), 400

    ai_brain.real_board = game_board
    
    best_col = ai_brain.get_best_move()
    
    if game_board.isvalidmove(best_col):
        game_board.makemove(best_col, 2)
        human_score = game_board.coount_connected_four(1) 
        ai_score = game_board.coount_connected_four(2)   
        game_over = game_board.isterminal()
        diff = game_board.get_difference(1, 2)
        winner = None
        if game_over:
            if diff > 0:
                winner = "Human"
            elif diff < 0:
                winner = "AI"
            else:
                winner = "Draw" 

        return jsonify({
            "grid": game_board.grid.tolist(),
            "ai_move": best_col,
            "game_over": game_over,
            "winner": winner,
            "human_score": human_score,
            "ai_score": ai_score   
        })

    return jsonify({"grid": game_board.grid.tolist(), "game_over": False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)