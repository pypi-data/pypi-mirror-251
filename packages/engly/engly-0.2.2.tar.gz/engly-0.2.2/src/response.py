from libs.common import json_open, path

resp = json_open(path("response.json"))

eng = input("英文:")

for key, value in resp.items():
    if key == eng:
        print("tag: " + value["tag"] + "\n" + value["response"])