#!/usr/bin/env python
import os
import sys
import requests
import json
import yaml
# Used to generate Content-MD5 which is used by Roblox to check data integrity
import base64, hashlib

ROBLOX_API_KEY = os.environ["ROBLOX_API_KEY"]
UNIVERSE_ID = 3138032475
BASE_URL = f"https://apis.roblox.com/datastores/v1/universes/{UNIVERSE_ID}"
DATASTORE_NAME = "Schedule"
DATASTORE_KEY = "Schedule"

scheduleJson = None
with open(os.environ["SCHEDULE_PATH"], "r", encoding="utf-8") as f:
    schedule = yaml.safe_load(f)
    scheduleJson = json.dumps(schedule)

contentMd5 = str(base64.b64encode(hashlib.md5(bytes(scheduleJson, encoding="utf8")).digest()), encoding="utf8")

headers = {
    'x-api-key': ROBLOX_API_KEY,
    'content-md5': contentMd5,
}

response = requests.post(
    f"{BASE_URL}/standard-datastores/datastore/entries/entry?datastoreName={DATASTORE_NAME}&entryKey={DATASTORE_KEY}",
    headers=headers,
    data=scheduleJson,
)

if response.status_code != 200:
    sys.exit(response.text) # Prints the content of the response and returns exit code 1