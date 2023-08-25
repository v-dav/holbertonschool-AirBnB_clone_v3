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



@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenityPlaceId(place_id, amenity_id):
    """Deletes amenity object in Place if found"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)

    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)

    if the_place not in the_amenity.place_amenities:
        abort(404)
    storage.delete(the_amenity)
    storage.save()
    return {}, 200


# @app_views.route("/places/<place_id>/reviews", methods=["POST"],
#                  strict_slashes=False)
# def create_review(place_id):
#     """Creates a review"""

#     """Check and get existing place"""
#     the_place = storage.get(Place, place_id)
#     if the_place is None:
#         abort(404)

#     """Check HTTP body request"""
#     http_body_request = request.get_json(silent=True)
#     if http_body_request is None:
#         return "Not a JSON\n", 400
#     elif "user_id" not in http_body_request:
#         return "Missing user_id\n", 400
#     elif "text" not in http_body_request:
#         return "Missing text\n", 400
#     else:
#         """Check user_id"""
#         the_user = storage.get(User, http_body_request["user_id"])
#         if the_user is None:
#             abort(404)
#         http_body_request["place_id"] = place_id

#         """Create new review"""
#         new_review = Review(**http_body_request)
#         storage.new(new_review)
#         storage.save()
#         return jsonify(new_review.to_dict()), 201
