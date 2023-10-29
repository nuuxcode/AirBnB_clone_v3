#!/usr/bin/python3
"""define routes of blueprint
"""

from api.v1.views import app_views


@app_views.route("/status", methods=['GET'])
def status():
    return {
        "status": "OK",
        }