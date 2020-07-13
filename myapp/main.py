from flask import Blueprint, request

from .controllers import controller

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        """
        Selama test request body yang dimasukan hanya actionnya saja tanpa model
        
        """
        return controller(request.get_json())
    return "ok", 200
