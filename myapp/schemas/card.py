from marshmallow import pre_load, EXCLUDE

from ..extensions import ma 
from ..models.card import CardModel

class CardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CardModel
        include_fk = True
        load_instance = True
        unknown = EXCLUDE

    @pre_load
    def parsing(self, input_data, **kwargs):
        """
        parsing nested field 
        card.id, card.name,
        list.id 
        board.id 
        add webhook_body key value
        """
        return {
            "id"      : input_data.get("data", {}).get("card", {}).get("id"),
            "name"    : input_data.get("data", {}).get("card", {}).get("name"),
            "list_id" : input_data.get("data", {}).get("list", {}).get("id"),
            "board_id": input_data.get("data", {}).get("board", {}).get("id"),
            "webhook_body": input_data
            }
