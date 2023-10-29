#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request
import json


def validateJSON(jsonData):
    try:
        if isinstance(jsonData, str):
            json.loads(jsonData)
        else:
            json.dumps(jsonData)
    except (json.JSONDecodeError, TypeError):
        return False
    return True


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """show states and states with id"""
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
    """delete method"""
    obj = storage.get(State, state_id)
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
    data = request.get_json(force=True)
    if not validateJSON(data):
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return new_state.to_dict(), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id):
    """update state"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True)
    if not validateJSON(data):
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return obj.to_dict(), 200
