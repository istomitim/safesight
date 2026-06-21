import requests
from django.conf import settings
import base64
import time
import os
import uuid
from playwright.sync_api import sync_playwright

# Ask VirusTotal about a file by its hash
def check_hash_on_virustotal(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}

    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code == 200:
        stats = response.json()["data"]["attributes"]["last_analysis_stats"]
        malicious = stats["malicious"]
        if malicious > 0:
            return f"Dangerous ({malicious} engines flagged it)"
        return "Clean"

    if response.status_code == 404:
        return "Unknown (not in VirusTotal database)"

    return "Check failed"


## Ask VirusTotal about a URL( two steps: submit, fetch)
def check_url_on_virustotal(url_to_check):
    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}

    # Step 1: submit the URL for analysis (POST = sending data)
    submit = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data={"url": url_to_check},
        timeout=15,
    )
    if submit.status_code != 200:
        return "Check failed"


    # Report ID is the URL encoded in base64 (API requirement)
    url_id = base64.urlsafe_b64encode(url_to_check.encode()).decode().strip("=")

    time.sleep(3)

    # Step 2: fetch the analysis report by that ID
    report = requests.get(
        f"https://www.virustotal.com/api/v3/urls/{url_id}",
        headers=headers,
        timeout=15,
    )
    if report.status_code != 200:
        return "Check failed"

    stats = report.json()["data"]["attributes"]["last_analysis_stats"]
    malicious = stats["malicious"]
    if malicious > 0:
        return f"Dangerous ({malicious} engines flagged it)"
    return "Clean"

# Web screenshot 
def take_screenshot(url_to_capture):
    filename = f"{uuid.uuid4().hex}.png" # generate unique file name
    filepath = os.path.join(settings.MEDIA_ROOT, "screenshots", filename)

    # Protection against broken sites
    try:
        # Playwright - launch invisible Chromium
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url_to_capture, timeout=15000, wait_until="domcontentloaded")
            page.screenshot(path=filepath)
            browser.close()
        return f"screenshots/{filename}"
    except Exception:
        return None