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

    board_id = db.Column(db.String(), db.ForeignKey('board.id'))
    board = db.relationship('BoardModel')

    def save_to_db(self):
        print(f"\ndidalam model board_id {self.board_id}\n---------------------------------------------------------")
        print(f"\ndidalam model name {self.name}\n---------------------------------------------------------")

        db.session.add(self)
        db.session.commit()
