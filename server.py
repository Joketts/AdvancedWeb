# import needed library's
from flask import *
from cyoa_game import CYOAGame, story
from flask_sqlalchemy import *
from Database import db, ReviewsSaved

# initializing flask app specifying static folder & creating an instance of the CYOAGame
app = Flask(__name__, static_folder='Static')
game = CYOAGame(story)

# configuring SQL Alchemy, initializing it and associating it with the flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PlayerProgress.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ReviewsSaved.db'
db.init_app(app)
with app.app_context():
    db.create_all()


# Route to display index page
@app.route("/index")
def index():
    return render_template('index.html')


# Route to display index page but with different app route
@app.route("/")
def home():
    return render_template('index.html')


# Route to display game page, resets game before starting and calling current page information
@app.route("/index/game")
def game_page():
    game.reset_game()
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


# Route to run previously saved game for specific id
@app.route("/index/game_saved/<uid>", methods=['GET', 'POST'])
def game_page_saved(uid):
    game.reset_game()
    # Retrieve the Firebase user ID from the URL
    firebase_user_id = uid
    # Load the saved progress for the given user ID
    game.load_progress(firebase_user_id)
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


# Route to handle player choice in game
@app.route("/index/game/make_choice/<choice_name>")
def make_choice(choice_name):
    # Retrieves the result of choice made
    choice_result = game.make_choice(choice_name)

    # checks if game ended
    try:
        if choice_result.get('game_ended'):
            # Retrieves the collected items and displays them on the endpage.html
            collected_items = choice_result.get('collected_items')
            return render_template('endpage.html', collected_items=collected_items)
    except:
        # called game restarted because reset_game caused issues with make_choice function so had to add try: except:
        print('Game restarted')
    # Gets game content for current page after choice is made
    page_content = game.get_current_page_content()
    return render_template('gamepage.html', page_text=page_content['text'], choices=page_content['choices'])


# Route to save game for specific id
@app.route('/index/game/save_progress', methods=['POST'])
def save_progress():
    # Gets Firebase unique id from Json data in the request
    firebase_user_id = request.json.get('firebase_user_id')
    # saves progress passing through unique id
    game.save_progress(firebase_user_id)
    # returns indicator of success
    return jsonify(status='success')


# Route for resetting game
@app.route('/index/game/reset_game', methods=['POST'])
def reset_game():
    # resets game and updates page content
    content = game.reset_game()
    return jsonify(content=content)


# Route to render account page
@app.route("/index/account")
def account():
    return render_template('Account.html')


# Route to save users reviews into the database
@app.route("/index/account/reviews", methods=['POST'])
def save_reviews():
    # Gets Firebase unique id and user review from JSON data in request
    firebase_user_id = request.json.get('firebase_user_id')
    user_review = request.json.get('user_review')

    # checks if review exists already for user, if not save new entry
    reviews = ReviewsSaved.query.filter_by(player_id=firebase_user_id).first()
    if not reviews:
        reviews = ReviewsSaved(player_id=firebase_user_id)

    # updating the users reviews and committing changes to database
    reviews.reviews_saved = user_review
    db.session.add(reviews)
    db.session.commit()
    return jsonify(status='success')


# Route to get saved reviews from the database
@app.route("/index/account/reviews_get", methods=['GET'])
def get_reviews():
    # Gets all reviews from database
    reviews = ReviewsSaved.query.all()
    # creates a list containing both player_id and user_review
    reviews_list = [{
        'player_id': review.player_id,
        'user_review': review.reviews_saved
    } for review in reviews]
    # returns the list of reviews as a JSON response
    return jsonify(reviews_list)


# Run the flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0')
