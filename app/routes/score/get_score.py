from app import app, db
from app.models import Score
from app.routes.helper import validate_auth_token
from app.routes.score.helper import get_score_owner, parse_score_request
from flask import abort, jsonify, make_response, request

import json
import app.routes.score.constants as constants

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

# # Update Score Common function
# # Updates existing score from database based on score user_id and year
# @app.route('/score', methods=['GET'])
# @validate_auth_token
# def update_score_common(requester):
#     # Get Request Data
#     postRequest = json.loads(request.data)

#     # Get user and year
#     user = get_score_owner(postRequest)
#     year = postRequest[constants.YEAR]
    
#     if user is None:
#         abort(make_response(jsonify(message="User doesn't exist"), 400))
#     score = Score.query.filter_by(user_id = user.id, year = year).first()
#     if score is None:
#         abort(make_response(jsonify(message="Score for the user at that year doesn't exists"), 400))

#     # Execute update score
#     score = parse_score_request(score, postRequest)
#     db.session.commit()

#     # Return that request is successful
#     return jsonify({
#         'id': score.id,
#         'username': user.username,
#         'year': year,
#         'message': "Successfully updated score"
#     }), 200