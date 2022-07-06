from app.models import Score, User
from flask import abort, jsonify, make_response

import app.routes.score.constants as constants

# Get score owner
# Used when given user_id or username to get the user owning that score
def get_score_owner(request) -> User:
    # Form validation
    if constants.USER_ID not in request:
        user_id = None
        if constants.USERNAME not in request:
            abort(make_response(jsonify(message="Form is not complete. Missing user_id / username"), 400))
        else:
            username = request[constants.USERNAME]
    else:
        username = None
        user_id = request[constants.USER_ID]
    if constants.YEAR not in request:
        abort(make_response(jsonify(message="Form is not complete. Missing year"), 400))

    # Form content validation
    if user_id is not None:
        user = User.query.filter_by(id = user_id).first()
    else:
        user = User.query.filter_by(username = username).first()
    
    return user

# Parse score request
# Returns score data of a specific user in a specific year
def parse_score_request(score: Score, request) -> Score:
    if constants.POSITION in request:
        score.position = request[constants.POSITION]
    if constants.SKS1_SCORE in request:
        score.sks1_score = request[constants.SKS1_SCORE]
    if constants.SKS2_SCORE in request:
        score.sks2_score = request[constants.SKS2_SCORE]
    if constants.SKS3_SCORE in request:
        score.sks3_score = request[constants.SKS3_SCORE]
    if constants.SUPPORT_SCORE in request:
        score.support_score = request[constants.SUPPORT_SCORE]
    if constants.CLUSTER in request:
        score.cluster = request[constants.CLUSTER]
    
    return score
