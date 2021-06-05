import requests
import json

hdr = {"X-API-Key": "ce822455b5f84c2788bee768f8"}
req = requests.get("https://api.checkwx.com/metar/KCTJ/decoded", headers=hdr)

print(req.json()["data"][0]["flight_category"])
