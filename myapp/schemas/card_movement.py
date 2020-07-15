from marshmallow import pre_load, EXCLUDE

from ..helpers import to_datetime
from ..extensions import ma
from ..models.card_movement import CardMovementModel

class CardMovementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CardMovementModel
        include_relationships = True
        include_fk = True
        # load_instance = True
        unknown = EXCLUDE
        dateformat = '%Y-%m-%dT%H:%M:%S+07:00'
        additional = ('list_before_id',)

    @pre_load
    def parsing(self, input_data, **kwargs):
        """"
        parsing nested field
        card.id
        listAfter.id
        listBefore.id
        from_date generate from action_id
        action_id
        """
        parsed_data = {
            "action_id" : input_data.get("id"),
            "card_id": input_data.get("data", {}).get("card",{}).get("id"),
            "from_date": to_datetime(input_data.get("id"))
        } 
        translationKey = input_data.get('display', {}).get('translationKey') 
        if  translationKey == 'action_create_card':
            parsed_data['list_id'] = input_data.get("data", {}).get("list", {}).get('id')
        elif translationKey == 'action_move_card_from_list_to_list':
            parsed_data['list_id'] = input_data.get("data", {}).get("listAfter",{}).get("id")
            parsed_data['list_before_id'] = input_data.get("data", {}).get("listBefore",{}).get("id")
        return parsed_data
    
