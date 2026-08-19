import requests


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


def participated_in(username, target_contest):

    contests = get_contest_history(username)

    target_contest = target_contest.lower().strip()

    for contest in contests:

        contest_name = contest["contest"]["title"].lower()

        if target_contest in contest_name:

            return contest["attended"]

    return False
