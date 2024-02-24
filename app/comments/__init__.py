from flask import Blueprint

bp = Blueprint('comments', __name__, url_prefix='/comments')

from app.comments import routes  # noqa: F401
