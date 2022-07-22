from sqlalchemy import false
from app import app, db
from app.models import Score
from app.routes.helper import validate_auth_token
from app.routes.score.helper import get_score_owner, parse_score_request
from flask import abort, jsonify, make_response, request

import app.routes.score.constants as constants
import json
import pandas as pd

# Insert Score function
# Adds new score of a certain user in a certain year to database
@app.route('/score', methods=['POST'])
@validate_auth_token
def insert_score(requester):
    # Get Request Data
    postRequest = json.loads(request.data)

    # Get user and year
    user = get_score_owner(postRequest)
    year = postRequest[constants.YEAR]
    
    if user is None:
        abort(make_response(jsonify(message="User doesn't exist"), 400))
    if Score.query.filter_by(user_id = user.id, year = year).first() is not None:
        abort(make_response(jsonify(message="Score for the user at that year exists"), 400))

    # Execute insert score
    score = Score(user_id = user.id, year = year)
    score = parse_score_request(score, postRequest)
    db.session.add(score)
    db.session.commit()

    # Return that request is successful
    return jsonify({
        'username': user.username,
        'year': year,
        'message': "Successfully inserted new score"
    }), 200