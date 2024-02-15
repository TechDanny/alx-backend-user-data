#!/usr/bin/env python3
"""
logout
"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.app import auth


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """
    handle user logout
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
