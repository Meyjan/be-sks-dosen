from app import app, db
from app.models import KelompokKeahlian
from app.routes.helper import validate_auth_token_edit_access
from app.routes.kelompok_keahlian.helper import validate_kk_request
from flask import abort, jsonify, make_response, request

import app.routes._olddir_score.constants as constants
import json

# Insert Score function
# Adds new score of a certain user in a certain year to database
@app.route('/kelompok_keahlian', methods=['POST'])
@validate_auth_token_edit_access
def insert_kelompok_keahlian(requester):
    # Get kelom keahlian
    postRequest = json.loads(request.data)
    kk = validate_kk_request(postRequest)

    # Execute insert score
    db.session.add(kk)
    db.session.commit()

    # Return that request is successful
    return jsonify({
        'kode': kk.kode,
        'kepanjangan': kk.kepanjangan,
        'message': "Successfully inserted new kelompok keahlian"
    }), 200