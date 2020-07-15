from ..extensions import db

class CardMovementModel(db.Model):
    __tablename__ = "card_movement"

    action_id = db.Column(db.String(), primary_key=True)
    from_date = db.Column(db.DateTime(), nullable=False)
    until_date = db.Column(db.DateTime(), nullable=True)

    card_id = db.Column(db.String(), db.ForeignKey('card.id'), nullable=False) # jgn lupa tambahkan ini db.ForeignKey('card.id')
    card = db.relationship('CardModel')

    list_id = db.Column(db.String(), db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('ListModel')

    @classmethod
    def save_to_db(cls, **kwargs):
        print("Create Card movement")
        print(kwargs)
        db.session.add(cls(**kwargs))
        db.session.commit()

    @classmethod
    def update_until_date(cls, **kwargs):
        data = kwargs
        print("data\n", data)
        print("kwargs before\n", kwargs["list_before_id"])
        old_movement = cls.query.filter_by(
            card_id=kwargs["card_id"], 
            list_id=kwargs["list_before_id"],
            until_date=None).first()
        if old_movement:
            print("ketemu")
            old_movement.until_date = kwargs["from_date"]
            db.session.commit()

        kwargs.pop("list_before_id")
        new_movement = cls(**kwargs)
        db.session.add(new_movement)
        db.session.commit()