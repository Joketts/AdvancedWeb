from flask import Flask, render_template, jsonify
from cyoa_game import CYOAGame, story
from flask_sqlalchemy import *
from Database import db

app = Flask(__name__)
game = CYOAGame(story)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PlayerProgress.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/index/game")
def game_page():
    game.reset_game()
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


@app.route("/index/game_saved")
def game_page_saved():
    game.reset_game()
    player_id = ''
    game.load_progress(player_id)
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


@app.route("/index/game/make_choice/<choice_name>")
def make_choice(choice_name):
    game.make_choice(choice_name)
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


@app.route('/index/game/go_back', methods=['POST'])
def go_back():
    content = game.go_back()
    return jsonify(content=content)


@app.route('/index/game/save_progress', methods=['POST'])
def save_progress():
    # Assuming 'game' is an instance of your CYOAGame class
    player_id = ''  # Replace with your logic to identify the player

    game.save_progress(player_id)  # Call the save_progress method from your CYOAGame instance

    return jsonify(status='success')  # Return a JSON response to indicate success


@app.route('/index/game/reset_game', methods=['POST'])
def reset_game():
    content = game.reset_game()
    return jsonify(content=content)


@app.route("/index/account")
def account():
    return render_template('Account.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
