from google_sheets import (
    get_students,
    get_history
)
from datetime import datetime

def calculate_statistics():

    students = get_students()

    codechef_history = get_history(
        "CodeChef History"
    )

    leetcode_history = get_history(
        "LeetCode History"
    )

    def get_recent_status(history, roll_no):

        student_records = [
            record
            for record in history
            if str(record["Roll No"]).strip() == roll_no
        ]
    
        # Keep only the latest record for each contest
        unique_contests = {}
    
        for record in student_records:
        
            contest = record["Contest"].strip()
    
            unique_contests[contest] = record
    
    
        # Keep only records that have a contest date
        dated_contests = [
            record
            for record in unique_contests.values()
            if record.get("Contest Date", "").strip()
        ]
    
    
        if not dated_contests:
            return "⚪ No Data"
    
    
        def parse_contest_date(record):
        
            date_string = record["Contest Date"].strip()
    
            # CodeChef:
            # 2026-08-12T22:00:00+05:30
            try:
                return datetime.fromisoformat(
                    date_string.replace("Z", "+00:00")
                ).replace(tzinfo=None)
    
            except ValueError:
                pass
            
            
            # LeetCode:
            # 2026-08-16 20:00:00
            try:
                return datetime.strptime(
                    date_string,
                    "%Y-%m-%d %H:%M:%S"
                )
    
            except ValueError:
                return datetime.min
    
    
        # Sort by actual contest date
        dated_contests.sort(
            key=parse_contest_date
        )
    
    
        # Take the latest three contests
        recent_contests = dated_contests[-3:]
    
    
        participated = sum(
            "Participated" in record["Participation"]
            for record in recent_contests
        )
    
    
        if participated == 0:
            return "🔴 Inactive"
    
        elif participated < len(recent_contests):
            return "🟡 Low Activity"
    
        else:
            return "🟢 Active"

    # --------------------------------
    # Create a dictionary for students
    # --------------------------------

    statistics = {}

    for student in students:

        roll_no = str(student["Roll No"]).strip()

        statistics[roll_no] = {
            "Roll No": student["Roll No"],
            "Name": student["Name"],
            "Section": student["Section"],

            "CodeChef Contests": 0,
            "CodeChef Attended": 0,

            "LeetCode Contests": 0,
            "LeetCode Attended": 0
        }

    # --------------------------------
    # Process CodeChef history
    # --------------------------------

    for record in codechef_history:

        roll_no = str(
            record["Roll No"]
        ).strip()

        if roll_no not in statistics:
            continue

        statistics[roll_no][
            "CodeChef Contests"
        ] += 1

        if "Participated" in record["Participation"]:
            statistics[roll_no][
                "CodeChef Attended"
            ] += 1

    # --------------------------------
    # Process LeetCode history
    # --------------------------------

    for record in leetcode_history:

        roll_no = str(
            record["Roll No"]
        ).strip()

        if roll_no not in statistics:
            continue

        statistics[roll_no][
            "LeetCode Contests"
        ] += 1

        if "Participated" in record["Participation"]:
            statistics[roll_no][
                "LeetCode Attended"
            ] += 1

    # --------------------------------
    # Calculate percentages
    # --------------------------------

    results = []

    for student in statistics.values():

        cc_contests = student[
            "CodeChef Contests"
        ]

        cc_attended = student[
            "CodeChef Attended"
        ]

        lc_contests = student[
            "LeetCode Contests"
        ]

        lc_attended = student[
            "LeetCode Attended"
        ]

        cc_percentage = (
            (cc_attended / cc_contests) * 100
            if cc_contests > 0
            else 0
        )

        lc_percentage = (
            (lc_attended / lc_contests) * 100
            if lc_contests > 0
            else 0
        )

        total_contests = cc_contests + lc_contests
        total_attended = cc_attended + lc_attended

        overall_percentage = (
            (total_attended / total_contests) * 100
            if total_contests > 0
            else 0
        )


        if overall_percentage >= 75:
            status = "🟢 Good"

        elif overall_percentage >= 50:
            status = "🟡 Average"

        else:
            status = "🔴 Needs Attention"

        cc_recent = get_recent_status(
            codechef_history,
            str(student["Roll No"]).strip()
        )

        lc_recent = get_recent_status(
            leetcode_history,
            str(student["Roll No"]).strip()
        )    

        results.append({
            "Roll No": student["Roll No"],
            "Name": student["Name"],
            "Section": student["Section"],

            "CodeChef Contests": cc_contests,
            "CodeChef Attended": cc_attended,
            "CodeChef %": round(cc_percentage, 2),

            "LeetCode Contests": lc_contests,
            "LeetCode Attended": lc_attended,
            "LeetCode %": round(lc_percentage, 2),

            "Overall %": round(overall_percentage, 2),
            "Status": status,

            "CC Recent": cc_recent,
            "LC Recent": lc_recent
        })

    return results
# if __name__ == "__main__":

#     from google_sheets import write_statistics

#     results = calculate_statistics()

#     write_statistics(results)

#     print(
#         f"\nStatistics generated for "
#         f"{len(results)} students."
#     )