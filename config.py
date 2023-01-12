import json

SETTINGS = {
	"title": "KeyRepeat",
	"icon": "favicon.png",
	"MIN_WIDTH": 500,
	"MIN_HEIGHT": 50,
	"pin_to_top": "True"
}

DEFAULT_NAME = "config.json"

def create_config():
    json_object = json.dumps(SETTINGS, indent=4)

    with open(DEFAULT_NAME, "w", encoding="utf-8") as f:
        f.write(json_object)
