from flask import Flask, render_template, jsonify

from AdvancedWeb.cyoa_game import CYOAGame, story

app = Flask(__name__)
game = CYOAGame(story)


@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/index/game/")
def game_page():
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


@app.route("/index/game/make_choice/<choice_name>")
def make_choice(choice_name):
    game.make_choice(choice_name)
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


@app.route('/go_back', methods=['POST'])
def go_back():
    content = game.go_back()
    return jsonify(content=content)
#
@app.route("/index/account/")
def account():
    return render_template('Account.html')


@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't Find page requested, Sorry.", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
