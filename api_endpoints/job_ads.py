def getAdResponse(results):
    if results.count() == 0:
        return {"success": False, "reason": "no job ad with this id"}, 400
    else:
        job_ads = []
        for result in results:
            job_ad = {}
            job_ad["id"] = result["_id"]
            job_ad["title"] = result["title"]
            job_ad["salary"] = result["salary"]
            job_ad["description"] = result["description"]

            if "applicants" in result:
                job_ad["applicants"] = result["applicants"]

            job_ads.append(job_ad)

        response = {
            "success": True,
            "job_ads": job_ads
        }
        return response


def addAdResponse(request):
    # check if request is json
    if request.content_type != 'application/json':
        return {"success": False, "reason": "content type is not application json"}, 400
    # check if there is a body in request
    if not request.data:
        return {"success": False, "reason": "missing body"}, 400

    # check if there are missing parameters in the request body
    missing = []
    if "title" not in request.json:
        missing.append("title")
    if "salary" not in request.json:
        missing.append("salary")
    if "description" not in request.json:
        missing.append("description")
    # return list of missing parameters if there are any
    if missing:
        response = {
            "success": False,
            "reason": "missing parameters",
            "missing": missing
        }
        return response, 400

    # check if the types of the body are correct
    if type(request.json["title"]) is not str:
        return {"success": False, "reason": "title not a string"}, 400
    if type(request.json["salary"]) is not int:
        return {"success": False, "reason": "salary not an int"}, 400
    if type(request.json["description"]) is not str:
        return {"success": False, "reason": "description not a string"}, 400

    # return 200 if there is no problem with request
    return 200


def editAdResponse(request):
    # check if request is json
    if request.content_type != 'application/json':
        return {"success": False, "reason": "content type is not application json"}, 400
    # check if there is a body in request
    if not request.data:
        return {"success": False, "reason": "missing body"}, 400

    something_to_update = False
    if "title" in request.json:
        something_to_update = True
    if "salary" in request.json:
        something_to_update = True
    if "description" in request.json:
        something_to_update = True

    if something_to_update:
        if "title" in request.json and type(request.json["title"]) is not str:
            return {"success": False, "reason": "title is not a string"}, 400
        if "salary" in request.json and type(request.json["salary"]) is not int:
            return {"success": False, "reason": "salary is not an int"}, 400
        if "description" in request.json and type(request.json["description"]) is not str:
            return {"success": False, "reason": "description is not string"}, 400
    else:
        return {"success": False, "reason": "missing parameters to update"}, 400

    # create update query if everything went ok
    updated_ad = {}
    updated_applications = {}
    if "title" in request.json:
        updated_ad["title"] = request.json["title"]
        updated_applications["applications.$.title"] = request.json["title"]
    if "salary" in request.json:
        updated_ad["salary"] = request.json["salary"]
        updated_applications["applications.$.salary"] = request.json["salary"]
    if "description" in request.json:
        updated_ad["description"] = request.json["description"]
        updated_applications["applications.$.description"] = request.json["description"]

    return updated_ad, updated_applications, 200
