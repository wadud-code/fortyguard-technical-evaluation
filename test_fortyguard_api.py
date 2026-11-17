
import json
import os
import time
import requests

API_KEY = os.environ.get("FORTYGUARD_API_KEY")
if not API_KEY:
    raise ValueError("Set FORTYGUARD_API_KEY in your terminal first!")

HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json",
}

# Small polygon around the Hialeah/Miami hotspot from the Dashboard

payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-80.260, 25.868],
                        [-80.245, 25.868],
                        [-80.245, 25.880],
                        [-80.260, 25.880],
                        [-80.260, 25.868],
                    ]],
                },
            }
        ],
    },
    "date_time": {
        "start_date": "2022-01-19",  # Matching the demo date or any date >= 2019-01-01
        "filter_type": 3             # Single Day (covers 00:00 - 23:59)
    }
}



print("1. Submitting heatmap task to FortyGuard API...")
submit_res = requests.post(
    "https://api.fortyguard.com/v1/heatmap",
    headers=HEADERS,
    json=payload,
)
print("HTTP Status:", submit_res.status_code)
print("Submit Response:", json.dumps(submit_res.json(), indent=2))

submit_res.raise_for_status()
activity_id = submit_res.json()["data"]["activity_id"]
print(f"\n2. Polling status for activity_id: {activity_id}")

for attempt in range(30):
    status_res = requests.get(
        f"https://api.fortyguard.com/v1/status/{activity_id}",
        headers={"api-key": API_KEY},
    )
    status_data = status_res.json().get("data", {})
    state = status_data.get("status", "").lower()
    print(f"   Attempt {attempt + 1}: status = {state}")

    if state in ("completed", "succeeded"):
        with open("miami_heatmap_result.json", "w") as f:
            json.dump(status_res.json(), f, indent=2)
        print("\nSuccess! Saved output to miami_heatmap_result.json")
        break
    elif state in ("failed", "error"):
        raise RuntimeError(f"Task failed: {status_data}")
    time.sleep(5)
