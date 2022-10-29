import os
import json


def dispatcher(client, method="get", url="/empty", data=None, headers=None, auth=None):

    if auth and not headers:
        headers = {"Authorization": "bearer " + auth}

    match method:
        case "post":
            data = json.dumps(data)
            response = client.post(url, data=data, headers=headers)
        case "put":
            data = json.dumps(data)
            response = client.put(url, data=data, headers=headers)
        case "patch":
            data = json.dumps(data)
            response = client.patch(url, data=data, headers=headers)
        case "delete":
            data = json.dumps(data)
            response = client.delete(url, headers=headers)
        case "form":
            response = client.post(url, data=data, headers=headers)
        case "files":
            # in this case we assume that data variable contains list of files
            files = data
            if isinstance(files, str):
                stream = open(files, "rb")
                files_data = {"uploads": (os.path.basename(files), stream, "image/png")}

            elif isinstance(files, list):
                files_data = []
                for path in files:
                    stream = open(path, "rb")
                    item = ("uploads", (os.path.basename(path), stream, "image/png"))
                    files_data.append(item)

            response = client.post(url, files=files_data, headers=headers)
        case _:  # default 'get'
            response = client.get(url, headers=headers)

    return response.status_code, response.json()


def get(client, url, headers=None, auth=None):
    return dispatcher(client, "get", url, None, headers, auth)


def post(client, url, data, headers=None, auth=None):
    return dispatcher(client, "post", url, data, headers, auth)


def put(client, url, data, headers=None, auth=None):
    return dispatcher(client, "put", url, data, headers, auth)


def patch(client, url, data, headers=None, auth=None):
    return dispatcher(client, "patch", url, data, headers, auth)


def delete(client, url, headers=None, auth=None):
    return dispatcher(client, "delete", url, None, headers, auth)


def postFiles(client, url, files, headers=None, auth=None):
    return dispatcher(client, "files", url, files, headers, auth)


def postForm(client, url, data, headers=None, auth=None):
    return dispatcher(client, "form", url, data, headers, auth)
