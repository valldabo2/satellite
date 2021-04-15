from project import app
from flask import jsonify, request
from project.models.fire import Fire
from manage import _create_db, _seed_db
from project import db
import json

API_PREFIX = '/api/'


@app.route("/")
def hello():
    return jsonify(message="Hello")


@app.route(f"{API_PREFIX}initialize/")
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


@app.route(f"{API_PREFIX}fires/<id>/", methods=['DELETE'])
def delete_fire(id):
    result = Fire.query.get(id)
    message = f"Not found {id}"
    if result:
        db.session.delete(result)
        message = f"Deleted {id}"
        db.session.commit()
    return jsonify(message=message)


@app.route(f"{API_PREFIX}fires/", methods=['POST'])
def post_fire():
    body = request.get_json()
    new_fire = Fire(**body)
    db.session.add(new_fire)
    db.session.commit()
    db.session.refresh(new_fire)
    return jsonify(convert_fire_to_json(new_fire))


@app.route(f"{API_PREFIX}fires/update", methods=['POST'])
def update_fires():
    fires = Fire.query.all()

    tileid_to_coordinates = {}
    with open('services/webapp/tiles_metadata.json') as f:
        data = json.load(f)
        for rec in data:
            long_lat = rec['center'].replace("POINT (", "").replace(")", "").split(" ")
            # "title": "S2A_MSIL1C_20200723T184921_N0209_R113_T10TFM_20200723T223737",
            shot_date = rec['title'].split("_")[2]
            shot_date_end = rec['title'].split("_")[6]
            tileid_to_coordinates[rec['tileid']] = {"longitude": float(long_lat[0]), "latitude": float(long_lat[1]),
                                                    "cloud": float(rec["cloudcoverpercentage"])}

    for fire in fires:
        tileid = fire.location.split("_")[1]
        print(f"Changing for {tileid} from {fire.longitude},{fire.latitude} to {tileid_to_coordinates[tileid]}")
        fire.longitude = tileid_to_coordinates[tileid]["longitude"]
        fire.latitude = tileid_to_coordinates[tileid]["latitude"]
        fire.cloud_coverage = tileid_to_coordinates[tileid]["cloud"]

        # Uncomment this to save to DB
        # db.session.commit()

    return jsonify(message="updated")
