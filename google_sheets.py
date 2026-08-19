import gspread
from datetime import datetime

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1imhnQSZ7cYuzBuNxCgwZObdX4UNyg-_nlA0CZK5DkE8/edit?resourcekey=&gid=1124545737#gid=1124545737"
RESPONSE_SHEET_NAME = "Form responses 1"
MONITORING_SHEET_NAME = "Contest Monitoring"
CODECHEF_HISTORY_SHEET = "CodeChef History"
LEETCODE_HISTORY_SHEET = "LeetCode History"
STATISTICS_SHEET = "Statistics"


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
        if str(student["Roll No"]).strip()
        or str(student["Name"]).strip()
    ]

    # Keep only the latest submission for each Roll No
    unique_students = {}

    for student in students:
        roll_no = str(student["Roll No"]).strip()

        if roll_no:
            unique_students[roll_no] = student

    students = list(unique_students.values())

    students.sort(
        key=lambda student: student["Name"].strip().lower()
    )

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

# CodeChef History
def save_codechef_history(results):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(CODECHEF_HISTORY_SHEET)

    existing_records = worksheet.get_all_records()

    existing_keys = set()

    for record in existing_records:
        key = (
            str(record["Roll No"]).strip(),
            record["Contest"].strip()
        )

        existing_keys.add(key)

    rows_to_add = []

    checked_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for result in results:

        key = (
            str(result["Roll No"]).strip(),
            result["Contest"].strip()
        )

        if key in existing_keys:
            continue

        rows_to_add.append([
        result["Roll No"],
        result["Name"],
        result["Section"],
        result["CodeChef ID"],
        result["Contest"],
        result["Contest Date"],
        result["Participation"],
        checked_at
    ])

    if rows_to_add:
        worksheet.append_rows(rows_to_add)
        print(
            f"{len(rows_to_add)} CodeChef history records added."
        )
    else:
        print("No new CodeChef history records to add.")

# LeetCode History
def save_leetcode_history(results):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(LEETCODE_HISTORY_SHEET)

    existing_records = worksheet.get_all_records()

    existing_keys = set()

    for record in existing_records:
        key = (
            str(record["Roll No"]).strip(),
            record["Contest"].strip()
        )

        existing_keys.add(key)

    rows_to_add = []

    checked_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for result in results:

        key = (
            str(result["Roll No"]).strip(),
            result["Contest"].strip()
        )

        if key in existing_keys:
            continue

        rows_to_add.append([
            result["Roll No"],
            result["Name"],
            result["Section"],
            result["LeetCode ID"],
            result["Contest"],
            result["Contest Date"],
            result["Participation"],
            checked_at
        ])

    if rows_to_add:
        worksheet.append_rows(rows_to_add)
        print(
            f"{len(rows_to_add)} LeetCode history records added."
        )
    else:
        print("No new LeetCode history records to add.")

def get_history(sheet_name):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(sheet_name)

    return worksheet.get_all_records()

def write_statistics(results):

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        STATISTICS_SHEET
    )

    # Remove previous statistics
    worksheet.batch_clear(["A2:M"])

    rows = []

    for result in results:

        rows.append([
            result["Roll No"],
            result["Name"],
            result["Section"],
            result["CodeChef Contests"],
            result["CodeChef Attended"],
            result["CodeChef %"],
            result["LeetCode Contests"],
            result["LeetCode Attended"],
            result["LeetCode %"],
            result["Overall %"],
            result["Status"],
            result["CC Recent"],
            result["LC Recent"]
        ])

    if rows:

        worksheet.update(
            "A2",
            rows
        )