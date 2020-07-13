import psycopg2
from sqlalchemy.exc import IntegrityError 

from .extensions import db 
from .schemas.board import BoardSchema
from .schemas.card import CardSchema

board_schema = BoardSchema()
card_schema  = CardSchema()

def test(data):
    # print("\n-----------------------------------------------------------------\ndalam test")
    # print(data)
    new_board = board_schema.load(data, session=db.session)
    try:
        new_board.save_to_db()
    except:
        return 'error', 500
    return 'ok', 200

def action_create_card(request_body):
    new_card = card_schema.load(request_body, session=db.session)
    try:
        new_card.save_to_db()
    except IntegrityError as err:
        print("IntegrityError")
        print(err.__dict__.keys())
        if type(err.orig) == psycopg2.errors.ForeignKeyViolation:
        # print(err.orig.pgcode)
            return {"message": "violates foreignkey constrain"}, 400
    except Exception as err:
        print(err)
        return {"message":"error"}, 500
    return 'ok', 200

controllers = {
    "test": test,
    "action_create_card": action_create_card
}

def controller(translationKey, data):
    func = controllers.get(translationKey)
    if func:
        return func(data)
    error_message = f"undefined translationKey {translationKey}"
    print(error_message)
    return {"error": error_message}, 400