from app import app, db
from app.models import Score, User
from app.routes.helper import validate_auth_token
from flask import abort, jsonify, make_response, request

import json
import app.routes.score.constants as constants

# Insert Score function
# Adds new score of a certain user in a certain year to database
@app.route('/score', methods=['POST'])
@validate_auth_token
def insert_score(user):
    # Get Request Data
    postRequest = json.loads(request.data)
    
    # Form validation
    if constants.USER_ID not in postRequest:
        user_id = None
        if constants.USERNAME not in postRequest:
            abort(make_response(jsonify(message="Form is not complete. Missing user_id / username"), 400))
        else:
            username = postRequest[constants.USERNAME]
    else:
        username = None
        user_id = postRequest[constants.USER_ID]
    if constants.YEAR not in postRequest:
        abort(make_response(jsonify(message="Form is not complete. Missing year"), 400))

    # Form content validation
    if user_id is not None:
        user = User.query.filter_by(id = user_id).first()
    else:
        user = User.query.filter_by(username = username).first()
    year = postRequest[constants.YEAR]
    
    if user is None:
        abort(make_response(jsonify(message="User doesn't exist"), 400))
    if Score.query.filter_by(user_id = user.id, year = year).first() is not None:
        abort(make_response(jsonify(message="Score for the user at that year exists"), 400))

    # Execute insert score
    score = parse_insert_score_request(postRequest, user.id, year)
    db.session.add(score)
    db.session.commit()

    # Return that request is successful
    return jsonify({
        'username': user.username,
        'year': year,
        'message': "Successfully inserted new score"
    }), 200

# Parses insert score request
# Returns score data of a specific user in a specific year
def parse_insert_score_request(request, user_id, year):
    score = Score(user_id = user_id, year = year)
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
