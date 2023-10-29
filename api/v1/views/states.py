#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""


from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states():
    all_objs = storage.all(State).values()
    states_list = []
    for v in all_objs:
        states_list.append(v.to_dict())
    return states_list
