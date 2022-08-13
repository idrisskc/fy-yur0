
from flask import Blueprint
path1 = Blueprint('path1', __name__)
from controller.controller_venues import venues, search_venues, show_venue, create_venue_form,create_venue_submission, delete_venue, edit_venue,edit_venue_submission

path1.route('/')(venues)
path1.route('/search', methods=['POST'])(search_venues)
path1.route('/<int:venue_id>')(show_venue)
path1.route('/create', methods=['GET'])(create_venue_form)
path1.route('/create', methods=['POST'])(create_venue_submission)
path1.route('/<venue_id>', methods=['DELETE'])(delete_venue)
path1.route('/<int:venue_id>/edit', methods=['GET'])(edit_venue)
path1.route('/<int:venue_id>/edit', methods=['POST'])(edit_venue_submission)
