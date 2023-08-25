#!/usr/bin/python3
"""A view API for reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_amenities_place(place_id):
    """Get all amenities of a place"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    json_format = []
    for amenity in the_place.amenities:
        json_format.append(amenity.to_dict())
    return jsonify(json_format)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenityPlaceId(place_id, amenity_id):
    """Deletes amenity object in Place if found"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)

    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)

    if the_amenity not in the_place.amenities:
        abort(404)
    storage.delete(the_amenity)
    storage.save()
    return {}, 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def create_amenityInPlace(place_id, amenity_id):
    """Creates an amenity linked to a place"""

    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)

    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)

    if the_amenity in the_place.amenities:
        return jsonify(the_amenity.to_dict()), 200

    new_amenity = Amenity(id=amenity_id)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201
