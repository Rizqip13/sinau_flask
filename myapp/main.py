from flask import Blueprint, request

from .controllers import controller

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        request_body = request.get_json()
        return controller(request_body.get('translationKey'), request_body)
    return "ok", 200
