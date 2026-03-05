import json
from datetime import datetime

FILE = "farmer_reports.json"

def save_farmer_report(crop, issue, location):

    report = {
        "crop": crop,
        "issue": issue,
        "location": location,
        "timestamp": str(datetime.now())
    }

    with open(FILE, "r") as f:
        data = json.load(f)

    data.append(report)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return "Report saved"

print(save_farmer_report(
    "rice",
    "brown spots on leaves",
    "Ongole"
))

## Check near by reports 
def check_local_reports(location):

    with open(FILE, "r") as f:
        data = json.load(f)

    alerts = []

    for report in data:
        if report["location"].lower() == location.lower():
            alerts.append(report)

    return alerts

print(check_local_reports("Ongole"))

## Generate alert message

def generate_community_alert(location):

    reports = check_local_reports(location)

    if len(reports) == 0:
        return "No farmer alerts in your area."

    crop = reports[-1]["crop"]
    issue = reports[-1]["issue"]

    alert = f"Farmers in {location} reported {issue} in {crop} crops. Please inspect your field."

    return alert

print(generate_community_alert("Ongole"))