from flask import Blueprint

bp = Blueprint('crawl', __name__)

from . import routes
