from flask import Blueprint, jsonify, request

from . import db_session
from .users import User

blueprint = Blueprint("users_api", __name__, template_folder="templates")
user_parameters = [
            "id",
            "surname",
            "name",
            "age",
            "position",
            "speciality",
            "address",
            "email",
            "password",
        ]
user_parameters_ = user_parameters.copy()
user_parameters_[-1] = "modified_date"


@blueprint.route("/api/users")
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {"users": [item.to_dict(only=user_parameters_) for item in users]}
    )


@blueprint.route("" "/api/users/<users_id>", methods=["GET"])
def get_one_users(users_id):
    session = db_session.create_session()
    try:
        users = session.query(User).get(int(users_id))
    except ValueError:
        return jsonify({"error": "Not found"})
    if not users:
        return jsonify({"error": "Not found"})
    return jsonify(
        {"users": users.to_dict(only=user_parameters_)}
    )


@blueprint.route("/api/users", methods=["POST"])
def create_users():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(
        key in request.json
        for key in user_parameters
    ):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    if session.query(User).get(request.json["id"]):
        return jsonify({"error": "Id already exists"})
    users = User(
        id=request.json["id"],
        surname=request.json["surname"],
        name=request.json["name"],
        age=request.json["age"],
        position=request.json["position"],
        speciality=request.json["speciality"],
        address=request.json["address"],
        email=request.json["email"],
    )
    users.set_password(request.json["password"])
    session.add(users)
    session.commit()
    return jsonify({"success": "OK"})


@blueprint.route("/api/users/<users_id>", methods=["DELETE"])
def delete_users(users_id):
    session = db_session.create_session()
    try:
        users = session.query(User).get(int(users_id))
    except ValueError:
        return jsonify({"error": "Not found"})
    if not users:
        return jsonify({"error": "Not found"})
    session.delete(users)
    session.commit()
    return jsonify({"success": "OK"})


@blueprint.route("/api/users", methods=["PUT"])
def edit_users():
    if not request.json:
        return jsonify({"error": "Empty request"})
    session = db_session.create_session()
    try:
        user = session.query(User).get(request.json["id"])
    except KeyError:
        return jsonify({"error": "Need a user id for editing"})
    if not user:
        return jsonify({"error": "Id doesnt exists"})
    user.surname = request.json.get("surname", user.surname)
    user.name = request.json.get("name", user.name)
    user.age = request.json.get("age", user.age)
    user.position = request.json.get("position", user.position)
    user.speciality = request.json.get("speciality", user.speciality)
    user.address = request.json.get("address", user.address)
    user.email = request.json.get("email", user.email)
    session.commit()
    return jsonify({"success": "OK"})
