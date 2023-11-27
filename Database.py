from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PlayerProgress(db.Model):
    __tablename__ = 'player_progress'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(100), nullable=False)
    current_page = db.Column(db.String(100))
    vial_power = db.Column(db.Integer, default=0)
    runes_power = db.Column(db.Integer, default=0)
    token_power = db.Column(db.Integer, default=0)


class ReviewsSaved(db.Model):
    __tablename__ = 'reviews_table'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(100), nullable=False)
    reviews_saved = db.Column(db.String(200))
