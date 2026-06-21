# SafeSight

A web application for safely checking suspicious files and links without opening them on your own computer.

## Features

- **File scanning** — upload a file; the server computes its SHA-256 hash and checks it against the VirusTotal API, returning a verdict (Clean / Dangerous / Unknown).
- **Link checking** — submit a URL; it is checked via VirusTotal and opened in a headless browser (Playwright) to capture a safe screenshot, so the user never opens the site directly.
- **User accounts** — session-based authentication with a personal scan history for each user.
- **History dashboard** and **admin panel** for managing scans.
- **Automated tests** for the models and access control.

## Tech stack

- **Back end:** Django (Python)
- **Front end:** HTML, CSS, JavaScript
- **Database:** SQLite
- **External tools:** VirusTotal API, Playwright (headless browser)

## Setup

1. Create and activate a virtual environment:
python3 -m venv venv

source venv/bin/activate

2. Install dependencies:
pip install -r requirements.txt

playwright install chromium

3. Create a `.env` file in the project root with your VirusTotal API key:
VIRUSTOTAL_API_KEY=your_key_here

4. Apply database migrations:
python manage.py migrate

5. Run the development server:
python manage.py runserver

6. Open `http://127.0.0.1:8000/` in your browser.

## Running tests
python manage.py test

