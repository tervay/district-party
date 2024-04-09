import json
from flask import Flask, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with open("data/out/annual_infos.json", "r") as f:
    annual_infos = json.load(f)


@app.route("/district/<district_key>/annual_infos")
def district_annual_infos(district_key: str):
    if district_key not in annual_infos:
        abort(400, "no district")

    return annual_infos[district_key]


@app.route("/all/annual_infos")
def all_annual_infos():
    return annual_infos
