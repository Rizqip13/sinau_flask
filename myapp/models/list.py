from sqlalchemy.dialects.postgresql import JSONB

from ..extensions import db

class ListModel(db.Model):
    __tablename__ = "list"

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    closed = db.Column(db.Boolean, nullable=False, default=False)
    # webhook_body = db.Column(JSONB, nullable=True)

    cards = db.relationship('CardModel', lazy='dynamic')

    board_id = db.Column(db.String(), db.ForeignKey('board.id'), nullable=False)
    board = db.relationship('BoardModel')

    def save_to_db(self): # ternyata ini tuh upsert yah
        db.session.add(self)
        db.session.commit()
