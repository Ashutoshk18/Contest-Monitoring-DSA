import requests
from datetime import datetime

def get_contest_history(username):

    url = "https://leetcode.com/graphql/"

    query = """
    query userContestRankingInfo($username: String!) {
        userContestRanking(username: $username) {
            attendedContestsCount
            rating
            globalRanking
        }

        userContestRankingHistory(username: $username) {
            attended
            rating
            ranking
            problemsSolved

            contest {
                title
                startTime
            }
        }
    }
    """

    variables = {
        "username": username
    }

    payload = {
        "query": query,
        "variables": variables,
        "operationName": "userContestRankingInfo"
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=15
        )
    except requests.RequestException as error:
        raise Exception(f"Network error: {error}")

    if response.status_code != 200:
        raise Exception(
            f"LeetCode returned status {response.status_code}"
        )

    data = response.json()

    if "errors" in data:
        raise Exception(
            "LeetCode returned an API error"
        )

    history = data["data"]["userContestRankingHistory"]

    if history is None:
        raise Exception(
            "LeetCode contest data not found"
        )

    return history

def get_contest_details(target_contest):

    url = "https://alfa-leetcode-api.onrender.com/contests"

    response = requests.get(
        url,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    contests = data["allContests"]

    target = target_contest.lower().strip()

    for contest in contests:

        if target == contest["title"].lower():

            contest_date = datetime.fromtimestamp(
                contest["startTime"]
            ).strftime("%Y-%m-%d %H:%M:%S")

            return {
                "name": contest["title"],
                "slug": contest["titleSlug"],
                "start_time": contest["startTime"],
                "date": contest_date
            }

    return None

def participated_in(username, target_contest):

    contests = get_contest_history(username)

    target_contest = target_contest.lower().strip()

    for contest in contests:

        contest_name = contest["contest"]["title"].lower()

        if target_contest in contest_name:

            return contest["attended"]

    return False

def get_contest(username, target_contest):

    contests = get_contest_history(username)

    target_contest = target_contest.lower().strip()

    for contest in contests:

        contest_name = (
            contest["contest"]["title"].lower()
        )

        if target_contest in contest_name:
            return contest

    return None