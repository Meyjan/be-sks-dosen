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

# Insert Score CSV function
# Adds new score of a certain user in a certain year to database
# Uploads csv files and inserts possible entrees into the database
@app.route('/score/csv', methods=['POST'])
@validate_auth_token
def insert_score_csv(requester):
    # Get Request Data
    if constants.FILE not in request.files:
        abort(make_response(jsonify(message="File doesn't exist"), 400))
    file = request.files[constants.FILE]

    commit_all_valid_data = false
    if constants.COMMIT_ALL_VALID in request.form:
        commit_all_valid_data = request.form[constants.COMMIT_ALL_VALID]
    
    # Read uploaded file and validate
    try:
        df = pd.read_csv(file)
    except:
        abort(make_response(jsonify(message="Unable to read the uploaded file"), 400))
    
    column_names = [constants.USER_ID, constants.YEAR, constants.POSITION, constants.SKS1_SCORE, constants.SKS2_SCORE, constants.SKS3_SCORE, constants.SUPPORT_SCORE, constants.CLUSTER]
    missing_columns = list()
    column_list = list(df.columns)
    for column_name in column_names:
        if column_name not in list(column_list):
            missing_columns += [column_name]
    if len(missing_columns) > 0:
        str_missing_columns = ', '.join(missing_columns)
        error_msg = "Missing columns in uploaded file: " + str_missing_columns
        abort(make_response(jsonify(message=error_msg), 400))
    
    # Put into database
    df.to_sql(Score.__tablename__, con = db.get_engine(), if_exists='append', index=False)



    # postRequest = json.loads(request.data)

    # # Get user and year
    # user = get_score_owner(postRequest)
    # year = postRequest[constants.YEAR]
    
    # if user is None:
    #     abort(make_response(jsonify(message="User doesn't exist"), 400))
    # if Score.query.filter_by(user_id = user.id, year = year).first() is not None:
    #     abort(make_response(jsonify(message="Score for the user at that year exists"), 400))

    # # Execute insert score
    # score = Score(user_id = user.id, year = year)
    # score = parse_score_request(score, postRequest)
    # db.session.add(score)
    # db.session.commit()

    # Return that request is successful
    return jsonify({
        'message': "Successfully inserted new scores"
    }), 200