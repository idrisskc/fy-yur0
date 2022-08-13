
from flask import Blueprint
path2 = Blueprint('path2', __name__)
from controller.controller_artists import artists, search_artists, show_artist,edit_artist,edit_artist_submission, create_artist_form, create_artist_submission

path2.route('/artists')(artists)
path2.route('/artists/search', methods=['POST'])(search_artists)
path2.route('/artists/<int:artist_id>')(show_artist)
path2.route('/artists/<int:artist_id>/edit', methods=['GET'])(edit_artist)
path2.route('/artists/<int:artist_id>/edit', methods=['POST'])(edit_artist_submission)
path2.route('/artists/create', methods=['GET'])(create_artist_form)
path2.route('/artists/create', methods=['POST'])(create_artist_submission)
