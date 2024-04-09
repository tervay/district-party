import json
from flask import Flask, abort
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# with open("data/out/annual_infos.json", "r") as f:
#     annual_infos = json.load(f)

annual_infos = {}
root_dir = "data/out/"

for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)

    if os.path.isdir(subdir_path):
        annual_infos_path = os.path.join(subdir_path, "annual_info.json")
        if os.path.exists(annual_infos_path):
            with open(annual_infos_path, "r") as file:
                annual_data = json.load(file)
                annual_infos[subdir.split("/")[-1]] = annual_data


@app.route("/district/<district_key>/annual_infos")
def district_annual_infos(district_key: str):
    if district_key not in annual_infos:
        abort(400, "no district")

    return annual_infos[district_key]


@app.route("/all/annual_infos")
def all_annual_infos():
    return annual_infos
