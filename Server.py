from flask import Flask, render_template

app = Flask(__name__)


@app.route("/index/")
def index():
    return render_template('index.html')

@app.route("/index/game/")
def game_page():
    return "Game Page"

@app.route("/index/game/end_game/")
def end_Game():
    return "End Game Page"

@app.route("/index/account/")
def account():
    return render_template('Account.html')

@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't Find page requested, Sorry.", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')
