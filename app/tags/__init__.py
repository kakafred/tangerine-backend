from flask import Blueprint

bp = Blueprint('tags', __name__, url_prefix='/tags')

from app.tags import routes  # noqa: F401
