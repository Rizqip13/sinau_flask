from marshmallow import pre_load, EXCLUDE

from ..extensions import ma 
from ..models.board import BoardModel

class BoardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BoardModel
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    @pre_load
    def parsing(self, input_data, **kwargs):
        """
        add webhook_body key value
        """
        return {**input_data, "webhook_body": input_data}