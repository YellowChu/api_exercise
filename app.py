from pymongo import MongoClient
from flask import Flask, request

from api_endpoints.candidates import getCandidateResponse, addCandidateResponse, editCandidateResponse, addApplicationAndApplicant
from api_endpoints.job_ads import getAdResponse, addAdResponse, editAdResponse

########################################
# Connection String Provided by Author #
########################################
connection_string = "enter provided database connection string"

cluster = MongoClient(connection_string)
db = cluster["data_sentics"]

candidates_db = db["candidates"]
job_ads_db = db["job_ads"]
used_ids_db = db["used_ids"]

app = Flask(__name__)


@app.route('/api/v1.0/candidates/', defaults={'candidate_id': None})
@app.route('/api/v1.0/candidates/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    # check if input is correct
    if type(candidate_id) is str and not candidate_id.isnumeric():
        return {"success": False, "reason": "input not an int"}, 400

    # if no input, get all candidates, otherwise get just specified candidate
    if candidate_id is None:
        results = candidates_db.find()
    else:
        results = candidates_db.find({"_id": int(candidate_id)})
    # prepare response
    response = getCandidateResponse(results)
    return response


@app.route('/api/v1.0/candidates/', methods=['POST'])
def add_candidate():
    response = addCandidateResponse(request)
    # if 400 was returned, something went wrong
    # if 200 was returned, everything was ok
    if response != 200:
        return response

    # get last created candidate id
    last_id = 0
    for last_id_doc in used_ids_db.find({"_id": 0}):
        last_id = last_id_doc["last_candidate_id"]

    # add candidate to database
    candidate = {
        "_id": last_id + 1,
        "name": request.json["name"],
        "pay": request.json["pay"],
        "skills": request.json["skills"],
    }
    candidates_db.insert_one(candidate)

    # update last created candidate id
    used_ids_db.update_one({"_id": 0}, {"$set": {"last_candidate_id": last_id + 1}})
    # return created candidate
    return {"success": True, "candidate_id": last_id + 1}


@app.route('/api/v1.0/candidates/', defaults={'candidate_id': None})
@app.route('/api/v1.0/candidates/<candidate_id>', methods=['PUT'])
def edit_candidate(candidate_id):
    # check if input is correct
    if candidate_id is None:
        return {"success": False, "reason": "no input"}, 400
    if type(candidate_id) is str and not candidate_id.isnumeric():
        return {"success": False, "reason": "input not a number"}, 400

    # check if candidates exists
    candidates_resp = get_candidate(candidate_id)
    if 400 in candidates_resp:
        return candidates_resp[0]
    # if 400 returns, something went wrong
    response = editCandidateResponse(request)
    if 400 in response:
        return response

    # get update queries
    updated_candidate = response[0]
    updated_applicants = response[1]
    # update candidate
    candidates_db.update_one({"_id": int(candidate_id)}, {"$set": updated_candidate})
    # update candidate in job ads db if there are any
    candidates = candidates_resp["candidates"]
    if "applications" in candidates[0]:
        candidates_applications = candidates[0]["applications"]
        for job_ad in candidates_applications:
            query = {"_id": job_ad["id"], "applicants.id": int(candidate_id)}
            job_ads_db.update_one(query, {"$set": updated_applicants})

    return {"success": True}


@app.route('/api/v1.0/candidates/', defaults={'candidate_id': None})
@app.route('/api/v1.0/candidates/<candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    # check if input is correct
    if candidate_id is None:
        return {"success": False, "reason": "no input"}, 400
    if type(candidate_id) is str and not candidate_id.isnumeric():
        return {"success": False, "reason": "input not a number"}, 400

    # delete candidate from database
    candidates_db.delete_one({"_id": int(candidate_id)})

    return {"success": True}


@app.route('/api/v1.0/candidates/', defaults={'candidate_id': None, 'ad_id': None})
@app.route('/api/v1.0/candidates/<candidate_id>/job_application/<ad_id>')
def apply(candidate_id, ad_id):
    # check if input is correct
    if candidate_id is None or ad_id is None:
        return {"success": False, "reason": "missing input"}, 400
    if type(candidate_id) is str and not candidate_id.isnumeric():
        return {"success": False, "reason": "candidate id not an int"}, 400
    if type(ad_id) is str and not ad_id.isnumeric():
        return {"success": False, "reason": "job ad id not an int"}, 400

    # get the candidate and if there is none return 400
    candidates_resp = get_candidate(candidate_id)
    if 400 in candidates_resp:
        return candidates_resp[0]
    # get the job ad and if there is none return 400
    job_ads_resp = get_ad(ad_id)
    if 400 in job_ads_resp:
        return job_ads_resp[0]

    candidate = candidates_resp["candidates"][0]
    job_ad = job_ads_resp["job_ads"][0]

    # get query to update candidate and job ad
    updatedApplications, updatedApplicants = addApplicationAndApplicant(candidate, job_ad)

    # update candidate
    if updatedApplications:
        candidates_db.update_one({"_id": int(candidate_id)}, {"$set": updatedApplications})
    # update job ad
    if updatedApplicants:
        job_ads_db.update_one({"_id": int(ad_id)}, {"$set": updatedApplicants})

    return {"success": True}


@app.route('/api/v1.0/ads/', defaults={'ad_id': None})
@app.route('/api/v1.0/ads/<ad_id>', methods=['GET'])
def get_ad(ad_id):
    # check if input is correct
    if type(ad_id) is str and not ad_id.isnumeric():
        return {"success": False, "reason": "input not an int"}, 400

    # if no input, get all job ads, otherwise get just specified job ad
    if ad_id is None:
        results = job_ads_db.find()
    else:
        results = job_ads_db.find({"_id": int(ad_id)})
    # prepare response
    response = getAdResponse(results)
    return response


@app.route('/api/v1.0/ads/', methods=['POST'])
def add_ad():
    response = addAdResponse(request)
    # if 400 was returned, something went wrong
    # if 200 was returned, everything was ok
    if response != 200:
        return response

    # get last created candidate id
    last_id = 0
    for last_id_doc in used_ids_db.find({"_id": 0}):
        last_id = last_id_doc["last_ad_id"]

    # add candidate to database
    candidate = {
        "_id": last_id + 1,
        "title": request.json["title"],
        "salary": request.json["salary"],
        "description": request.json["description"],
    }
    job_ads_db.insert_one(candidate)

    # update last created candidate id
    used_ids_db.update_one({"_id": 0}, {"$set": {"last_ad_id": last_id + 1}})
    # return created candidate
    return {"success": True, "ad_id": last_id + 1}


@app.route('/api/v1.0/ads/', defaults={'ad_id': None})
@app.route('/api/v1.0/ads/<ad_id>', methods=['PUT'])
def edit_ad(ad_id):
    # check if input is correct
    if ad_id is None:
        return {"success": False, "reason": "no input"}, 400
    if type(ad_id) is str and not ad_id.isnumeric():
        return {"success": False, "reason": "input not a number"}, 400

    # check if ad exists
    ads_resp = get_ad(ad_id)
    if 400 in ads_resp:
        return ads_resp[0]
    # if 400 returns, something went wrong
    response = editAdResponse(request)
    if 400 in response:
        return response

    # get update queries
    updated_ad = response[0]
    updated_applications = response[1]
    # update ad
    job_ads_db.update({"_id": int(ad_id)}, {"$set": updated_ad})
    # update applications in candidates db uf there are any
    job_ads = ads_resp["job_ads"]
    if "applicants" in job_ads[0]:
        job_ads_applicants = job_ads[0]["applicants"]
        for candidate in job_ads_applicants:
            query = {"_id": candidate["id"], "applications": int(ad_id)}
            candidates_db.update_one(query, {"$set": updated_applications})

    return {"success": True}


@app.route('/api/v1.0/ads/', defaults={'ad_id': None})
@app.route('/api/v1.0/ads/<ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    # check if input is correct
    if ad_id is None:
        return {"success": False, "reason": "no input"}, 400
    if type(ad_id) is str and not ad_id.isnumeric():
        return {"success": False, "reason": "input not a number"}, 400

    # delete candidate from database
    job_ads_db.delete_one({"_id": int(ad_id)})

    return {"success": True}


if __name__ == '__main__':
    app.run(debug=False)
