from flask import Blueprint

bp = Blueprint('closest_organisations', __name__)

from app.closest_organisations import routes