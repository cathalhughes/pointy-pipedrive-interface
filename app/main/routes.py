from app.main import bp
import requests
import json
from flask import render_template, request, redirect, url_for

f = open("app/key.txt", "r")
API_TOKEN = f.readline()

url = "https://api.pipedrive.com/v1/"
api  = "api_token=" + API_TOKEN

@bp.route('/')
def index():
    oragnisations_request = requests.get(url + "organizations?limit=5&start=0&" + api)
    organisations_json_data = json.loads(oragnisations_request.content)
    organisations_data = organisations_json_data["data"]
    organisation_objects = []
    for organisation in organisations_data:
        object = {"name": organisation["name"],
                  "id": organisation["id"],
                  "address_route": organisation["address_route"],
                  "address_country": organisation["address_country"],
                  "owner_name": organisation["owner_name"],
                  "address": organisation["address"]}
        organisation_objects.append(object)

    return render_template("index.html", organisation_objects=organisation_objects)

@bp.route('/delete/<id>')
def delete_organisation(id):
    delete_request = requests.delete(url + "organizations/" + id + "?" + api)
    delete_json_data = json.loads(delete_request.content)
    is_deleted = delete_json_data['success']
    response = {"is_deleted": is_deleted}
    return json.dumps(response)

@bp.route('/edit/<id>', methods=['POST'])
def edit_organisation(id):
    updated_info = request.form.getlist('info[]')
    name = updated_info[0]
    address_route = updated_info[1]
    address_country = updated_info[2]
    owner = updated_info[-1]
    updated_information = {"name": name,
                            "owner_name": owner,
                            "address_route": address_route,
                            "address_country": address_country}
    edit_request = requests.put(url + "organizations/" + id + "?" + api, data=updated_information)
    print(edit_request.status_code)
    return "Done"


@bp.route('/create', methods=["POST"])
def create():
    name = request.form["name"]
    address_route = request.form["address_route"]
    address_country = request.form["address_country"]
    owner = request.form["owner_name"]
    creation_information = {"name": name,
                           "address_route": address_route,
                           "address_country": address_country,
                            "owner_name": "Liam"}
    print(creation_information)
    creation_request = requests.post(url + "organizations?" + api, data=creation_information)
    print(creation_request.content)
    return redirect(url_for('main.index'))

@bp.route('/newpage')
def new_page():
    pass

