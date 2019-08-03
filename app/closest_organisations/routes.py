from app.closest_organisations import bp
import requests
import json
from flask import render_template, request, redirect, url_for
from math import cos, asin, sqrt

f = open("app/key.txt", "r")
API_TOKEN = f.readline().strip()

url = "https://api.pipedrive.com/v1/"
api  = "api_token=" + API_TOKEN

@bp.route("/closestorganisations")
def closest_organisations():
    return render_template("closest_organisations.html")

@bp.route('/getclosestorganisations', methods=["POST"])
def get_closest_organisations():
    longitude = float(request.form["longitude"])
    latitude = float(request.form["latitude"])
    v = {'lat': latitude, 'lon': longitude}
    organisations_with_distances = get_organisations_with_distances()
    closest_organisations = closest(organisations_with_distances, v)
    print(closest_organisations)
    return render_template("closest_organisations.html", organisation_objects=closest_organisations, longitude=longitude, latitude=latitude)

@bp.route("/printclosestorganisations", methods=["POST"])
def print_closest_organisations():
    longitude = float(request.form["longitude"])
    latitude = float(request.form["latitude"])
    v = {'lat': latitude, 'lon': longitude}
    organisations_with_distances = get_organisations_with_distances()
    closest_organisations = closest(organisations_with_distances, v)
    return render_template("print_closest_organisations.html", organisation_objects=closest_organisations, longitude=longitude, latitude=latitude)

def get_organisations_with_distances():
    oragnisations_request = requests.get(url + "organizations?" + api)
    organisations_json_data = json.loads(oragnisations_request.content.decode('utf-8'))
    organisations_data = organisations_json_data["data"]
    organisations_with_distances = []
    for organisation in organisations_data:
        coords = organisation["address"]
        if coords == None:
            continue
        coords = coords.split(",")
        if len(coords) != 2 or '' in coords:
            continue
        print(coords)
        object = {"name": organisation["name"],
                  "id": organisation["id"],
                  "id_num": organisation["a4d182c739831733f713026160af27d8c2cbea9c"],
                  "full_address": organisation["ae5ac9cd2a5608bddeb9a80abaf3a0220ed100b9"],
                  "url": organisation["42f105653b173b032024227247a380c5c98eb822"],
                  "store_type": organisation["475b0aa34d21dbf01357541a25fe683a9ebcc24b"],
                  "owner_name": organisation["owner_name"],
                  "owner_id": organisation["owner_id"]["id"],
                  "address": organisation["address"],
                  "lat": float(coords[0].strip()),
                  "lon": float(coords[1])}
        organisations_with_distances.append(object)
    print(organisations_with_distances)
    return organisations_with_distances

def haversine(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, v):
    return sorted(data, key=lambda p: haversine(v['lat'],v['lon'],p['lat'],p['lon']))[:5]

tempDataList = [{'lat': 39.7612992, 'lon': -86.1519681},
                {'lat': 39.762241,  'lon': -86.158436 },
                {'lat': 39.7622292, 'lon': -86.1578917}]


