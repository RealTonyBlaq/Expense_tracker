#!/usr/bin/env python3
""" The Admin routes """

from api.v1 import ETapp, admin_required
from flask import abort, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from models.tag import Tag
from utilities import db
from werkzeug.exceptions import BadRequest


@ETapp.route('/tags', strict_slashes=False)
@ETapp.route('/tags/<tag_id>', strict_slashes=False)
@jwt_required()
def get_tags(tag_id=None):
    """ Returns an object containing a list of Tag objects """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if tag_id:
        tag = db.query(Tag).filter_by(id=tag_id).first()
        if tag:
            return jsonify(message='success', data=tag.to_dict()), 200
        abort(404)

    all_tags = db.query(Tag).filter_by(user_id=current_user.id).all()
    tags = [tag.to_dict() for tag in all_tags]
    return jsonify(message='success', data=tags), 200


@ETapp.route('/tags', methods=['POST'], strict_slashes=False)
@jwt_required()
@admin_required
def create_tag():
    """ Creates a new Tag object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        if 'name' not in data:
            return jsonify(message='name missing'), 400

        new_tag = Tag(name=data['name'], user_id=current_user.id)
        new_tag.save()
        return jsonify(message='success', data=new_tag.to_dict()), 201

    return jsonify(message='Not a valid JSON'), 400


@ETapp.route('/tags/<tag_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
@admin_required
def update_tag(tag_id):
    """ Updates a Tag object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        tag = db.query(Tag).filter_by(id=tag_id).first()
        if not tag:
            abort(404)

        if 'name' not in data:
            return jsonify(message='name missing'), 400

        setattr(tag, 'name', data['name'])
        tag.save()
        return jsonify(message='success', data=tag.to_dict()), 200

    return jsonify(message='Not a valid JSON'), 400


@ETapp.route('/tags/<tag_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@admin_required
def delete_tag(tag_id):
    """ Deletes a Tag object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    tag = db.query(Tag).filter_by(id=tag_id).first()
    if not tag:
        abort(404)

    tag.delete()
    return jsonify(message='success'), 200
