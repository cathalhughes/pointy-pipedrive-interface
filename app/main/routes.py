from app.main import bp
import requests
import json
from flask import render_template, request, redirect, url_for, flash

f = open("app/key.txt", "r")
API_TOKEN = f.readline().strip()

url = "https://api.pipedrive.com/v1/"
api  = "api_token=" + API_TOKEN

@bp.route('/')
def index():
    oragnisations_request = requests.get(url + "organizations?limit=5&start=0&" + api)
    organisations_json_data = json.loads(oragnisations_request.content.decode('utf-8'))
    organisations_data = organisations_json_data["data"]
    organisation_objects = []
    for organisation in organisations_data:
        object = {"name": organisation["name"],
                  "id": organisation["id"],
                  "id_num": organisation["a4d182c739831733f713026160af27d8c2cbea9c"],
                  "full_address": organisation["ae5ac9cd2a5608bddeb9a80abaf3a0220ed100b9"],
                  "url": organisation["42f105653b173b032024227247a380c5c98eb822"],
                  "store_type": organisation["475b0aa34d21dbf01357541a25fe683a9ebcc24b"],
                  "owner_id": organisation["owner_id"]["id"],
                  "owner_name": organisation["owner_name"],
                  "address": organisation["address"]}
        organisation_objects.append(object)

    return render_template("index.html", organisation_objects=organisation_objects, start=5)

@bp.route('/getmoreorganisations', methods=["POST"])
def get_more_organisations():
    start = request.form["start"]
    new_start = int(start) + 5
    oragnisations_request = requests.get(url + "organizations?limit=5&start=" + start + "&" + api)
    organisations_json_data = json.loads(oragnisations_request.content.decode('utf-8'))
    organisations_data = organisations_json_data["data"]
    organisation_objects = []
    for organisation in organisations_data:
        object = {"name": organisation["name"],
                  "id": organisation["id"],
                  "id_num": organisation["a4d182c739831733f713026160af27d8c2cbea9c"],
                  "full_address": organisation["ae5ac9cd2a5608bddeb9a80abaf3a0220ed100b9"],
                  "url": organisation["42f105653b173b032024227247a380c5c98eb822"],
                  "store_type": organisation["475b0aa34d21dbf01357541a25fe683a9ebcc24b"],
                  "owner_id": organisation["owner_id"]["id"],
                  "owner_name": organisation["owner_name"],
                  "address": organisation["address"]}
        organisation_objects.append(object)

    return render_template("index.html", organisation_objects=organisation_objects, start=new_start)


@bp.route('/delete/<id>')
def delete_organisation(id):
    delete_request = requests.delete(url + "organizations/" + id + "?" + api)
    delete_json_data = json.loads(delete_request.content.decode('utf-8'))
    is_deleted = delete_json_data['success']
    response = {"is_deleted": is_deleted}
    return json.dumps(response)

@bp.route('/edit/<id>', methods=['POST'])
def edit_organisation(id):
    updated_info = request.form.getlist('info[]')
    name = updated_info[0]
    full_address = updated_info[1]
    id_num = updated_info[2]
    store_type = updated_info[3]
    updated_information = {"name": name,
                            "a4d182c739831733f713026160af27d8c2cbea9c": id_num,
                           "42f105653b173b032024227247a380c5c98eb822": "http://localhost:8080/internal/shop/" + id_num,
                            "ae5ac9cd2a5608bddeb9a80abaf3a0220ed100b9": full_address,
                            "475b0aa34d21dbf01357541a25fe683a9ebcc24b": store_type}
    edit_request = requests.put(url + "organizations/" + id + "?" + api, data=updated_information)
    edit_json_data = json.loads(edit_request.content.decode('utf-8'))
    is_edited = edit_json_data['success']
    response = {"is_edited": is_edited}
    return json.dumps(response)


@bp.route('/create', methods=["POST"])
def create():
    name = request.form["name"]
    full_address = request.form["full_address"]
    id_num = request.form["id_num"]
    store_type = request.form["store_type"]
    creation_information = {"name": name,
                           "a4d182c739831733f713026160af27d8c2cbea9c": id_num,
                           "42f105653b173b032024227247a380c5c98eb822": "http://localhost:8080/internal/shop/" + id_num,
                            "ae5ac9cd2a5608bddeb9a80abaf3a0220ed100b9": full_address,
                            "475b0aa34d21dbf01357541a25fe683a9ebcc24b": store_type}
    creation_request = requests.post(url + "organizations?" + api, data=creation_information)
    if creation_request.status_code != 201:
        flash("Creation failed!")
        return redirect(url_for('main.index'))

    data = json.loads(creation_request.content.decode('utf-8'))
    data = data["data"]
    id = data["id"]
    flash("Organisation created with ID: " + str(id))
    return redirect(url_for('main.index'))


