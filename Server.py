from flask import Flask, render_template, jsonify, request
from cyoa_game import CYOAGame, story
from flask_sqlalchemy import *
from Database import db, ReviewsSaved

app = Flask(__name__)
game = CYOAGame(story)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PlayerProgress.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ReviewsSaved.db'
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


@app.route("/index/game_saved/<uid>", methods=['GET', 'POST'])
def game_page_saved(uid):
    game.reset_game()
    firebase_user_id = uid
    game.load_progress(firebase_user_id)
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


@app.route("/index/game/make_choice/<choice_name>")
def make_choice(choice_name):
    choice_result = game.make_choice(choice_name)

    if choice_result.get('game_ended'):
        collected_items = choice_result.get('collected_items')
        return render_template('endpage.html', collected_items=collected_items)

    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


@app.route('/index/game/save_progress', methods=['POST'])
def save_progress():
    firebase_user_id = request.json.get('firebase_user_id')  # Retrieve Firebase user ID from the request

    game.save_progress(firebase_user_id)  # Call the save_progress method from your CYOAGame instance

    return jsonify(status='success')  # Return a JSON response to indicate success


@app.route('/index/game/reset_game', methods=['POST'])
def reset_game():
    content = game.reset_game()
    return jsonify(content=content)


@app.route("/index/account")
def account():
    return render_template('Account.html')


@app.route("/index/account/reviews", methods=['POST'])
def save_reviews():
    firebase_user_id = request.json.get('firebase_user_id')
    user_review = request.json.get('user_review')

    reviews = ReviewsSaved.query.filter_by(player_id=firebase_user_id).first()
    if not reviews:
        reviews = ReviewsSaved(player_id=firebase_user_id)
    reviews.reviews_saved = user_review
    db.session.add(reviews)
    db.session.commit()
    return jsonify(status='success')


@app.route("/index/account/reviews_get", methods=['GET'])
def get_reviews():
    reviews = ReviewsSaved.query.all()  # Retrieve all reviews from the database
    reviews_list = [{
        'player_id': review.player_id,
        'user_review': review.reviews_saved
    } for review in reviews]
    return jsonify(reviews_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
