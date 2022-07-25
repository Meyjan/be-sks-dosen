from app.models import KelompokKeahlian
from flask import abort, jsonify, make_response

import app.routes.kelompok_keahlian.const as const

# Get score owner
# Used when given user_id or username to get the user owning that score
def validate_kk_request(request) -> KelompokKeahlian:
    # Form validation
    if const.PARAM_KK_KODE not in request:
        abort(make_response(jsonify(message=f"Form is not complete. Missing parameter: {const.PARAM_KK_KODE}"), 400))
    if const.PARAM_KK_KEPANJANGAN not in request:
        abort(make_response(jsonify(message=f"Form is not complete. Missing parameter: {const.PARAM_KK_KEPANJANGAN}"), 400))

    # Form content validation
    kk = parse_kk_request(request)
    return kk

# Parse score request
# Returns score data of a specific user in a specific year
def parse_kk_request(request) -> KelompokKeahlian:
    kk = KelompokKeahlian()
    kk.kode = request[const.PARAM_KK_KODE]
    kk.kepanjangan = request[const.PARAM_KK_KEPANJANGAN]
    
    return kk
