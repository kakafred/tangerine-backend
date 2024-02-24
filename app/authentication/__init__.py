from flask import Blueprint

bp = Blueprint('authentication', __name__, url_prefix='/auth')

from app.authentication import routes  # noqa: F401
