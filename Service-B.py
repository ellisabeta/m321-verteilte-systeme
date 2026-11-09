"""Run with python service_b.py, then visit http://127.0.0.1:8001/."""

import json
from http.client import HTTPException
from urllib.request import urlopen
from wsgiref.simple_server import make_server


def fetch_people():
    base_url = "http://127.0.0.1:3000"
    with urlopen(base_url + "/people", timeout=5) as response:
        people = json.load(response)

    if not isinstance(people, list):
        raise ValueError("Expected a JSON list")
    entries = []
    for person in people:
        if not isinstance(person, dict) or not isinstance(person.get("name"), str):
            raise ValueError("Expected a person with a name")
        entry = person["name"]
        if person.get("age") is not None:
            entry += f" {person['age']}"
        if person.get("addr"):
            entry += f", {person['addr']}"
        entries.append(entry)
    return " | ".join(entries)


def app(request, start_response):
    status = "200 OK"
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    if request["REQUEST_METHOD"] != "GET":
        status, message = "405 Method Not Allowed", "Use GET."
        headers.append(("Allow", "GET"))
    elif request["PATH_INFO"] == "/":
        message = "Hello World from Service B!"
    elif request["PATH_INFO"] == "/ping":
        try:
            message = fetch_people()
        except (OSError, HTTPException):
            status, message = "502 Bad Gateway", "Could not get /people from Service A."
        except ValueError:
            status, message = "502 Bad Gateway", "Check Service A's URL and /people JSON format."
    else:
        status, message = "404 Not Found", "Route not found."
    start_response(status, headers)
    return [message.encode("utf-8")]


if __name__ == "__main__":
    with make_server("127.0.0.1", 8001, app) as server:
        print("Service B is running at http://127.0.0.1:8001/", flush=True)
        server.serve_forever()
