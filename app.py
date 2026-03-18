from flask import Flask, jsonify, request, send_from_directory
from engine import Game, Player
from cards import (get_fire_deck, get_death_deck, get_ice_deck,
                   get_life_deck, get_storm_deck, get_myth_deck)
import os

app = Flask(__name__)
game_instance = None

def get_or_create_game():
    global game_instance
    if game_instance is None:
        p1 = Player("Pyromancer Bob", "Fire", 6500)
        p1.deck = get_fire_deck()

        p2 = Player("Necromancer Alice", "Death", 7000)
        p2.deck = get_death_deck()

        game_instance = Game(p1, p2)
        game_instance.log(f"=== Match Start: {p1.name} vs {p2.name} ===")
    return game_instance

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/state', methods=['GET'])
def get_state():
    game = get_or_create_game()
    return jsonify(game.to_dict())

@app.route('/api/action', methods=['POST'])
def handle_action():
    game = get_or_create_game()
    data = request.json
    action = data.get('action')
    player = data.get('player')

    if player != game.turn:
        return jsonify({'error': 'Not your turn'}), 400

    success = False
    if action == 'draw_pip':
        success = game.draw_pip()
    elif action == 'cast_spell':
        card_id = data.get('card_id')
        target_name = data.get('target_name')
        success = game.cast_spell(card_id, target_name)
    elif action == 'discard_card':
        card_id = data.get('card_id')
        success = game.discard_card(card_id)
    elif action == 'enchant_card':
        enchant_id = data.get('enchant_card_id')
        target_id = data.get('target_card_id')
        success = game.enchant_card(enchant_id, target_id)
    elif action == 'pass_turn':
        game.pass_turn()
        success = True
    elif action == 'reset':
       global game_instance
       game_instance = None
       success = True

    return jsonify({'success': success, 'state': get_or_create_game().to_dict()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
