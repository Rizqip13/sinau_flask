from sqlalchemy.dialects.postgresql import JSONB

from ..extensions import db

class CardModel(db.Model):
    __tablename__ = "card"

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String())
    closed = db.Column(db.Boolean, nullable=False, default=False)
    webhook_body = db.Column(JSONB, nullable=True)
    # url = db.Column(db.String())

    list_id = db.Column(db.String(), db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('ListModel')

    board_id = db.Column(db.String(), db.ForeignKey('board.id'), nullable=False)
    board = db.relationship('BoardModel')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
