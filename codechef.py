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

def get_contest_details(target_contest):

    url = (
        "https://www.codechef.com/api/list/contests/all"
        "?mode=all"
        "&offset=0"
        "&sort_by=START"
        "&sorting_order=asc"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.codechef.com/contests"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    target = target_contest.lower().strip()

    all_contests = (
        data.get("present_contests", [])
        + data.get("future_contests", [])
        + data.get("practice_contests", [])
        + data.get("past_contests", [])
    )

    for contest in all_contests:

        if target in contest["contest_name"].lower():

            return {
                "name": contest["contest_name"],
                "code": contest["contest_code"],
                "start_date": contest["contest_start_date_iso"],
                "end_date": contest["contest_end_date_iso"]
            }

    return None

def participated_in(username, target_contest):
    contests = get_contest_history(username)

    target_contest = target_contest.lower().strip()

    for contest in contests:
        contest_name = contest["name"].lower()

        if target_contest in contest_name:
            return True

    return False

def get_contest(username, target_contest):

    contests = get_contest_history(username)

    target_contest = target_contest.lower().strip()

    for contest in contests:

        contest_name = contest["name"].lower()

        if target_contest in contest_name:
            return contest

    return None

def get_contest_date(target_contest):

    contests = get_contest_history(
        "decodester"
    )

    target_contest = target_contest.lower().strip()

    for contest in contests:

        contest_name = contest["name"].lower()

        if target_contest in contest_name:
            return contest["end_date"]

    return ""