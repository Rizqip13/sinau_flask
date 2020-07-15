from parse import *
import psycopg2
from sqlalchemy.exc import IntegrityError 

from .extensions import db 

from .models.card_movement import CardMovementModel

from .schemas.board import BoardSchema
from .schemas.card import CardSchema
from .schemas.list import ListSchema
from .schemas.card_movement import CardMovementSchema

board_schema = BoardSchema()
card_schema  = CardSchema()
list_schema  = ListSchema()
card_movement_schema = CardMovementSchema()

def test(data):
    # print("\n-----------------------------------------------------------------\ndalam test")
    # print(data)
    new_board = board_schema.load(data, session=db.session)
    try:
        new_board.save_to_db()
    except:
        return 'error', 500
    return 'ok', 200

def action_create_card(action):
    new_card = card_schema.load(action, session=db.session)
    card_movement = card_movement_schema.load(action, session=db.session)
    try:
        new_card.save_to_db()
        CardMovementModel.save_to_db(**card_movement)
    except IntegrityError as err:
        """
        This is okay for now,
        Nanti harus ditambahkan untuk create board dan list nya dahulu
        dan harus selalu return 200 kecuali bener2 error
        """
        if type(err.orig) == psycopg2.errors.ForeignKeyViolation:
            orig = search("Key ({})", str(err.orig))
            return {"message": str(err.orig)}, 400
    except Exception as err:
        print(err)
        return {"message": str(err)}, 500
    return 'ok', 200

def action_added_list_to_board(action):
    new_list = list_schema.load(action, session=db.session)
    try:
        new_list.save_to_db()
    except IntegrityError as err:
        """
        This is okay for now,
        Nanti harus ditambahkan untuk create board dan list nya dahulu
        dan harus selalu return 200 kecuali bener2 error
        """
        if type(err.orig) == psycopg2.errors.ForeignKeyViolation:
            orig = search("Key ({})", str(err.orig))
            return {"message": str(err.orig)}, 400
    except Exception as err:
        print(err)
        return {"message": str(err)}, 500
    return 'ok', 200

def action_move_card_from_list_to_list(action):
    new_card_movement = card_movement_schema.load(action, session=db.session)
    # print(new_card_movement)
    # new_card_movement.pop('list_before_id')
    # print(new_card_movement)
    # new = CardMovementModel(**new_card_movement)
    # new.save_to_db()
    CardMovementModel.update_until_date(**new_card_movement)
    return card_movement_schema.dump(new_card_movement), 200

controllers = {
    "test": test,
    "action_create_card": action_create_card,
    "action_added_list_to_board": action_added_list_to_board,
    "action_move_card_from_list_to_list": action_move_card_from_list_to_list
}

def controller(webhook_body):
    """
    disini bisa ditambahkan insert webhook_body ke database dan ambil id nya untuk fk controllers
    """
    action = webhook_body.get('action')
    func = controllers.get(action.get('display', {}).get("translationKey"))
    if func:
        return func(action)
    error_message = f"undefined translationKey {translationKey}"
    print(error_message)
    return {"error": error_message}, 400