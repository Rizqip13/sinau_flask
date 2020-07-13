from sqlalchemy.dialects.postgresql import JSONB

from ..extensions import db

class BoardModel(db.Model):
    __tablename__ = "board"

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String())
    closed = db.Column(db.Boolean, nullable=False, default=False)
    webhook_body = db.Column(JSONB, nullable=True)

    cards = db.relationship('CardModel', lazy='dynamic')

    def save_to_db(self): # ternyata ini tuh upsert yah
        db.session.add(self)
        db.session.commit()
