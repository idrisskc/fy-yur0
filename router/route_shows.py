
from flask import Blueprint
path3 = Blueprint('path3', __name__)
from controller.controller_shows import shows, create_shows, create_show_submission

path3.route('/')(shows)
path3.route('/create')(create_shows)
path3.route('/create', methods=['POST'])(create_show_submission)