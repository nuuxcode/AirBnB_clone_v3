#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
import os
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from flask import abort, request, jsonify

db_mode = os.getenv("HBNB_TYPE_STORAGE")

@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def place_amenities(place_id):
    """retrieve place amenities"""
    amenities_list = []
    place = storage.get(Place, place_id)
    if not place:
        abort(400)
    if db_mode == "db":
        amenities = place.amenities
        for amenity in amenities:
            amenities_list.append(amenity.to_dict())

    else:
        amenities_list = place.amenity_ids
    return jsonify(amenities_list)


