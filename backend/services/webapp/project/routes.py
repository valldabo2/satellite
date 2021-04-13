from project import app
from flask import jsonify, request
from project.models.fire import Fire
from manage import _create_db, _seed_db
from project import db

API_PREFIX = '/api/'


@app.route(f"{API_PREFIX}initialize")
def initialize():
    _create_db()
    _seed_db()
    return jsonify(message="Initialized DB")


@app.route(f"{API_PREFIX}fires/", methods=['GET'])
def get_fires():
    fires = Fire.query.all()
    result = []
    for fire in fires:
        fireJson = convert_fire_to_json(fire)
        result.append(fireJson)
    return jsonify(result)


def convert_fire_to_json(fire_object):
    res = dict(fire_object.__dict__)
    del res['_sa_instance_state']
    return res


@app.route(f"{API_PREFIX}fires/<id>/", methods=['GET'])
def get_fire(id):
    result = Fire.query.get(id)
    fireJson = convert_fire_to_json(result)
    return jsonify(fireJson)


@app.route(f"{API_PREFIX}fires/", methods=['POST'])
def post_fire():
    body = request.get_json()
    new_fire = Fire(**body)
    db.session.add(new_fire)
    db.session.commit()
    db.session.refresh(new_fire)
    return jsonify(convert_fire_to_json(new_fire))
