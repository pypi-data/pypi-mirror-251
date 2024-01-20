import requests


def make_req(prompt):
    headers = {
        "user_input": prompt
    }
    result = requests.post("https://api.encounterstrive.info.gf/vsoh/api/generate_response", json=headers)
    if result.status_code == 200:
        return result.json()['response']


def reset():
    result = requests.post("https://api.encounterstrive.info.gf/vsoh/api/reset_context")
    if result.status_code == 200:
        return True


def one():
    result = requests.get("https://api.encounterstrive.info.gf/vsoh/api/1")
    if result.status_code == 200:
        return result.json()


def two():
    result = requests.get("https://api.encounterstrive.info.gf/vsoh/api/2")
    if result.status_code == 200:
        return result.json()


def three():
    result = requests.get("https://api.encounterstrive.info.gf/vsoh/api/3")
    if result.status_code == 200:
        return result.json()


def four():
    result = requests.get("https://api.encounterstrive.info.gf/vsoh/api/4")
    if result.status_code == 200:
        return result.json()
