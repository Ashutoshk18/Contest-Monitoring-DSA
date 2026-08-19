import requests
from bs4 import BeautifulSoup
import re
import json
import time


def get_contest_history(username):
    url = f"https://www.codechef.com/users/{username}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )
    except requests.RequestException as error:
        raise Exception(f"Network error: {error}")

    if response.status_code == 404:
        raise Exception("CodeChef username not found")

    if response.status_code != 200:
        raise Exception(
            f"CodeChef returned status {response.status_code}"
        )

    soup = BeautifulSoup(response.text, "html.parser")

    script = soup.find(
        "script",
        string=lambda text: (
            text and "date_versus_rating" in text
        )
    )

    if not script:
        raise Exception("Contest data not found")

    script_text = script.string

    match = re.search(
        r'"date_versus_rating":(\{.*?\}),'
        r'"user_initial_ratings"',
        script_text
    )

    if not match:
        raise Exception("Could not extract contest data")

    try:
        contest_data = json.loads(match.group(1))
    except json.JSONDecodeError:
        raise Exception("Could not parse contest data")

    return contest_data["all"]


def participated_in(username, target_contest):
    contests = get_contest_history(username)

    target_contest = target_contest.lower().strip()

    for contest in contests:
        contest_name = contest["name"].lower()

        if target_contest in contest_name:
            return True

    return False