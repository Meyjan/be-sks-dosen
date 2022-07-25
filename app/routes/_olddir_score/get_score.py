from app import app
from app.models import Score
from app.routes.helper import validate_auth_token
from app.routes._olddir_score.helper import get_score_owner, parse_score_request
from flask import abort, jsonify, make_response, request

import json
import app.routes._olddir_score.constants as constants

# Get Score function
# Gets existing score from database based on score id
@app.route('/score/<int:score_id>', methods=['GET'])
@validate_auth_token
def get_score(requester, score_id):
    # Get score
    score = Score.query.filter_by(id = score_id).first()
    if score is None:
        abort(make_response(jsonify(message="Score id doesn't exist"), 400))

    # Return that request is successful
    return jsonify({
        'score': score.as_dict(),
        'message': "Successfully get score"
    }), 200

# Get Score Common function
# Gets existing score from database based on score user_id and year
@app.route('/score', methods=['GET'])
@validate_auth_token
def get_score_common(requester):
    # Get Request Data
    args = request.args

    # Get filters
    filter_keys = [constants.ID, constants.USER_ID, constants.YEAR, constants.POSITION, constants.SKS1_SCORE, constants.SKS2_SCORE, constants.SKS3_SCORE, constants.SUPPORT_SCORE, constants.CLUSTER]
    filtered_args = dict([(key, value) for key, value in args.items() if key in filter_keys])

    # Get score
    scores = Score.query.filter_by(**filtered_args).all()
    scores_dict = [score.as_dict() for score in scores]

    # Return that request is successful
    return jsonify({
        'score': scores_dict,
        'message': "Successfully get score"
    }), 200