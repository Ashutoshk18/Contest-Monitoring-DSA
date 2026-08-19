import requests
from datetime import datetime


url = "https://alfa-leetcode-api.onrender.com/contests"

response = requests.get(
    url,
    timeout=15
)

print("Status:", response.status_code)

data = response.json()

contests = data["allContests"]

print("Total contests:", len(contests))


for contest in contests:

    if contest["title"] == "Weekly Contest 498":

        contest_date = datetime.fromtimestamp(
            contest["startTime"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        print("\nFOUND!")

        print("Name:", contest["title"])
        print("Slug:", contest["titleSlug"])
        print("Unix timestamp:", contest["startTime"])
        print("Contest date:", contest_date)

        break

else:
    print("\nWeekly Contest 498 not found.")
    