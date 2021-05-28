# API Exercise
API created using Flask framework and MongoDB. There are two endpoints:
*candidates*, *ads*. You can store, receive, edit and delete job
candidates and job ads. Also there is a candidate endpoint to store
information when candidate applies for a job.

## Getting started
1. Install dependencies in *requirements.txt*
2. Enter provided database connection string in *line 10* in *app.py*
    ```python
   cluster = MongoClient("enter provided database connection string")
    ```
3. Run *app.py*
4. Server runs on *localhost:5000*

## Endpoints
### Candidates
| Method | Path                                                      | Function                                        |
|--------|-----------------------------------------------------------|-------------------------------------------------|
| GET    | /api/v1.0/candidates/<br/>/api/v1.0/candidates/<candidate_id> | Gets all candidates<br/> Gets picked candidate |
| POST   | /api/v1.0/candidates/                                     | Creates new candidate                           |
| PUT    | /api/v1.0/candidates/<candidate_id>                       | Updates picked candidate                        |
| DELETE | /api/v1.0/candidates/                                     | Deleted picked candidate                        |
##### Candidate job application (GET method)
```
/api/v1.0/candidates/<candidate_id>/job_application/<ad_id>
```
Will create list of job ads that candidate has applied to and list of candidates that job ad has received.

### Job Ads
| Method | Path                                 | Function                                  |
|--------|--------------------------------------|-------------------------------------------|
| GET    | /api/v1.0/ads/<br/> /api/v1.0/ads/<ad_id> | Gets all job ads<br/> Gets picked job ad |
| POST   | /api/v1.0/ads/                       | Creates new job ad                        |
| PUT    | /api/v1.0/ads/<ad_id>               | Updates picked job ad                     |
| DELETE | /api/v1.0/ads/                       | Deleted picked job ad                     |

## Examples
After you initialized your local server with *app.py*, you can send HTTP requests to it.
Here are examples of sending requests to the API using Python.
### Get candidate with ID=1
##### Request:
```python
import requests
import json

url = "http://localhost:5000/api/v1.0/candidates/1"

response = requests.get(url)
respContent = json.loads(response.content)
print(respContent)
```
##### Response:
```json
{
    "candidates": [
        {
            "id": 1,
            "name": "Peter Parker",
            "pay": 99,
            "skills": [
                "physics",
                "photography"
            ]
        }
    ],
    "success": true
}
```

### Create new candidate
* Header **Content-Type** has to be set to **application/json**
* Request body has to contain:
    * name *string*
    * pay *int*
    * skills *list of strings*.
##### Request:
```python
import requests
import json

url = "http://localhost:5000/api/v1.0/candidates/"
body = {
    "name": "Bruce Wayne",                  
    "pay": 12000,                         
    "skills": ["entrepreneur", "tech"]      
}

response = requests.post(url, json=body)
respContent = json.loads(response.content)
print(respContent)
```
##### Response:
```json
{
    "candidate_id": 2,
    "success": true
}
```

### Update candidate with ID=2
Similar to creating a new candidate, but now you have to specify candidate id in url.
##### Request:
```python
import requests
import json

url = "http://localhost:5000/api/v1.0/candidates/2"
body = {
    "name": "Tony Stark"
}

response = requests.put(url, json=body)
respContent = json.loads(response.content)
print(respContent)
```

### Create new job ad
* Header **Content-Type** has to be set to **application/json**.
* Request body has to contain: 
    * title *string*
    * salary *int*
    * description *string*
##### Request:
```python
import requests
import json

url = "http://localhost:5000/api/v1.0/ads/"
body = {
    "title": "Super Hero",                  
    "salary": 0,                         
    "description": "Helping people."      
}

response = requests.post(url, json=body)
respContent = json.loads(response.content)
print(respContent)
```
##### Response:
```json
{
    "ad_id": 1,
    "success": true
}
```

### Candidate (with candidate ID=2) applies to a job ad (with ad ID=1)
Creates a list of job ads in candidate and list of candidates in job ad.
##### Request:
```python
import requests
import json

url = "http://localhost:5000/api/v1.0/candidates/2/job_application/1"

response = requests.get(url)
respContent = json.loads(response.content)
print(respContent)
```
##### GET candidate with ID=2 Response:
```json
{
    "candidates": [
        {
            "applications": [
                {
                    "description": "Helping people.",
                    "id": 1,
                    "salary": 0,
                    "title": "Super Hero"
                }
            ],
            "id": 2,
            "name": "Tony Stark",
            "pay": 12000,
            "skills": [
                "entrepreneur",
                "tech"
            ]
        }
    ],
    "success": true
}
```
##### GET job ad with ID=1 Response:
```json
{
    "job_ads": [
        {
            "applicants": [
                {
                    "id": 2,
                    "name": "Tony Stark",
                    "pay": 12000,
                    "skills": [
                        "entrepreneur",
                        "tech"
                    ]
                }
            ],
            "description": "Helping people.",
            "id": 1,
            "salary": 0,
            "title": "Super Hero"
        }
    ],
    "success": true
}
```
