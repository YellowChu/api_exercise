def getCandidateResponse(results):
    if results.count() == 0:
        return {"success": False, "reason": "no candidate with this id"}, 400
    else:
        candidates = []
        for result in results:
            candidate = {}
            candidate["id"] = result["_id"]
            candidate["name"] = result["name"]
            candidate["pay"] = result["pay"]
            candidate["skills"] = result["skills"]
            if "applications" in result:
                candidate["applications"] = result["applications"]

            candidates.append(candidate)

        response = {
            "success": True,
            "candidates": candidates
        }
        return response


def addCandidateResponse(request):
    # check if request is json
    if request.content_type != 'application/json':
        return {"success": False, "reason": "content type is not application json"}, 400
    # check if there is a body in request
    if not request.data:
        return {"success": False, "reason": "missing body"}, 400

    # check if there are missing parameters in the request body
    missing = []
    if "name" not in request.json:
        missing.append("name")
    if "pay" not in request.json:
        missing.append("pay")
    if "skills" not in request.json:
        missing.append("skills")
    # return list of missing parameters if there are any
    if missing:
        response = {
            "success": False,
            "reason": "missing parameters",
            "missing": missing
        }
        return response, 400

    # check if the types of the body are correct
    if type(request.json["name"]) is not str:
        return {"success": False, "reason": "name not a string"}, 400
    if type(request.json["pay"]) is not int:
        return {"success": False, "reason": "pay not an int"}, 400
    if type(request.json["skills"]) is not list:
        return {"success": False, "reason": "skills not a list"}, 400
    if len(request.json["skills"]) is 0:
        return {"success": False, "reason": "skills list is empty"}, 400
    for skill in request.json["skills"]:
        if type(skill) != str:
            return {"success": False, "reason": "listed skill is not a string"}, 400

    # return 200 if there is no problem with request
    return 200


def editCandidateResponse(request):
    # check if request is json
    if request.content_type != 'application/json':
        return {"success": False, "reason": "content type is not application json"}, 400
    # check if there is a body in request
    if not request.data:
        return {"success": False, "reason": "missing body"}, 400

    something_to_update = False
    if "name" in request.json:
        something_to_update = True
    if "pay" in request.json:
        something_to_update = True
    if "skills" in request.json:
        something_to_update = True

    if something_to_update:
        if "name" in request.json and type(request.json["name"]) is not str:
            return {"success": False, "reason": "name is not a string"}, 400
        if "pay" in request.json and type(request.json["pay"]) is not int:
            return {"success": False, "reason": "pay is not an int"}, 400
        if "skills" in request.json:
            if type(request.json["skills"]) is not list:
                return {"success": False, "reason": "skills is not a list"}, 400
            for skill in request.json["skills"]:
                if type(skill) is not str:
                    return {"success": False, "reason": "listed skill is not a string"}, 400
    else:
        return {"success": False, "reason": "missing parameters to update"}, 400

    # create update query if everything went ok
    updated_candidate = {}
    updated_applicants = {}
    if "name" in request.json:
        updated_candidate["name"] = request.json["name"]
        updated_applicants["applicants.$.name"] = request.json["name"]
    if "pay" in request.json:
        updated_candidate["pay"] = request.json["pay"]
        updated_applicants["applicants.$.pay"] = request.json["pay"]
    if "skills" in request.json:
        updated_candidate["skills"] = request.json["skills"]
        updated_applicants["applicants.$.skills"] = request.json["skills"]

    return updated_candidate, updated_applicants, 200


def addApplicationAndApplicant(candidate, job_ad):
    updatedApplications = {}
    if "applications" in candidate:
        isNew = True
        for application in candidate["applications"]:
            if job_ad["id"] is application["id"]:
                isNew = False
        if isNew:
            updatedApplications["applications"] = candidate["applications"]
            newApplication = {
                "id": job_ad["id"],
                "title": job_ad["title"],
                "salary": job_ad["salary"],
                "description": job_ad["description"]
            }
            updatedApplications["applications"].append(newApplication)
    else:
        newApplication = {
            "id": job_ad["id"],
            "title": job_ad["title"],
            "salary": job_ad["salary"],
            "description": job_ad["description"]
        }
        updatedApplications["applications"] = [newApplication]

    updatedApplicants = {}
    if "applicants" in job_ad:
        isNew = True
        for applicant in job_ad["applicants"]:
            if candidate["id"] is applicant["id"]:
                isNew = False
        if isNew:
            updatedApplicants["applicants"] = job_ad["applicants"]
            newApplicant = {
                "id": candidate["id"],
                "name": candidate["name"],
                "pay": candidate["pay"],
                "skills": candidate["skills"]
            }
            updatedApplicants["applicants"].append(newApplicant)
    else:
        newApplicant = {
            "id": candidate["id"],
            "name": candidate["name"],
            "pay": candidate["pay"],
            "skills": candidate["skills"]
        }
        updatedApplicants["applicants"] = [newApplicant]

    return updatedApplications, updatedApplicants




