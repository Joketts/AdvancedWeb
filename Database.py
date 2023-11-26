from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PlayerProgress(db.Model):
    __tablename__ = 'player_progress'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(100), nullable=False)  # Assuming you have some way to identify players
    current_page = db.Column(db.String(100))
