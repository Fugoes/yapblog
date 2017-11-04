from flask import request, jsonify, abort

from yapb import app, db
from yapb.models import User


@app.route("/api/user", methods=["GET", "POST"])
def api_user():
    if request.method == "GET":
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    elif request.method == "POST":
        try:
            new_user = User(request.form["name"], request.form["email"])
        except KeyError:
            return abort(404)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict())
    else:
        return abort(404)
