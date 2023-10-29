#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""


from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    states_list = []
    if state_id is None:
        all_objs = storage.all(State).values()
        for v in all_objs:
            states_list.append(v.to_dict())
        return states_list
    else:
        result = storage.get(State, state_id)
        if result is None:
            abort(404)
        return result.to_dict()


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def states_delete(state_id):
    obj = storage.get(State, state_id)
    print(obj)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    if storage.get(State, state_id) is None:
        return {}, 200
    else:
        return "Delete fail"


@app_views.route("/states", strict_slashes=False,
                 methods=["POST"])
def create_state():
    """create a new post req"""
    data = request.get_json()
    if data is None:
        abort(400)
    new_state = State(**data)
    new_state.save()
    return new_state.to_dict(), 201
