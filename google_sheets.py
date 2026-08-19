import gspread


SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1imhnQSZ7cYuzBuNxCgwZObdX4UNyg-_nlA0CZK5DkE8/edit?resourcekey=&gid=1124545737#gid=1124545737"
RESPONSE_SHEET_NAME = "Form responses 1"
MONITORING_SHEET_NAME = "Contest Monitoring"


def get_spreadsheet():
    client = gspread.service_account(
        filename="credentials.json"
    )

    return client.open_by_url(SPREADSHEET_URL)


def get_students():
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(RESPONSE_SHEET_NAME)

    students = worksheet.get_all_records()

    # Remove completely empty rows
    students = [
        student
        for student in students
        if student["Roll No"] or student["Name"]
    ]

    return students


def get_target_codechef_contest():
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(MONITORING_SHEET_NAME)

    return worksheet.acell("B1").value


def get_target_leetcode_contest():
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(MONITORING_SHEET_NAME)

    return worksheet.acell("B2").value


def write_results(results):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(MONITORING_SHEET_NAME)

    # Remove previous results while keeping
    # the contest information and headers intact.
    worksheet.batch_clear(["A4:G"])

    # Prepare rows
    rows = []

    for student in results:
        rows.append([
            student["Roll No"],
            student["Name"],
            student["Section"],
            student["CodeChef ID"],
            student["LeetCode ID"],
            student["CodeChef Participation"],
            student["LeetCode Participation"],
        ])

    # Write all rows at once
    if rows:
        worksheet.update(
            "A4",
            rows
        )