from marshmallow import pre_load, EXCLUDE

from ..extensions import ma 
from ..models.list import ListModel

class ListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ListModel
        include_relationships = True
        include_fk = True
        load_instance = True
        unknown = EXCLUDE

    @pre_load
    def parsing(self, input_data, **kwargs):
        """
        parsing nested field 
        list.id, list.name
        board.id
        add webhook_body key value
        """
        return {
            "id"      : input_data.get("data", {}).get("list", {}).get("id"),
            "name"    : input_data.get("data", {}).get("list", {}).get("name"),
            "board_id": input_data.get("data", {}).get("board", {}).get("id"),
            # "webhook_body": input_data
            }