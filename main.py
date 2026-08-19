import time
from google_sheets import (
    get_students,
    get_target_codechef_contest,
    get_target_leetcode_contest,
    write_results,
    save_codechef_history,
    save_leetcode_history,
    write_statistics
)

from codechef import participated_in as codechef_participated
from leetcode import participated_in as leetcode_participated

from stats import calculate_statistics



students = get_students()

codechef_contest = get_target_codechef_contest()
leetcode_contest = get_target_leetcode_contest()

print(f"CodeChef contest: {codechef_contest}")
print(f"LeetCode contest: {leetcode_contest}")
print(f"Students found: {len(students)}\n")


results = []
codechef_history = []
leetcode_history = []

for student in students:

    name = student["Name"]
    codechef_id = student["CodeChef ID"]
    leetcode_id = student["LeetCode ID"]

    # -------------------------
    # CodeChef
    # -------------------------

    if codechef_id:

        try:
            participated = codechef_participated(
                codechef_id,
                codechef_contest
            )

            if participated:
                codechef_status = "✅ Participated"
            else:
                codechef_status = "❌ Did not participate"

        except Exception as error:
            codechef_status = f"⚠️ {error}"

    else:
        codechef_status = "⚠️ ID not provided"

    codechef_history.append({
        "Roll No": student["Roll No"],
        "Name": name,
        "Section": student["Section"],
        "CodeChef ID": codechef_id,
        "Contest": codechef_contest,
        "Participation": codechef_status
    })


    # -------------------------
    # LeetCode
    # -------------------------

    if leetcode_id:

        try:
            participated = leetcode_participated(
                leetcode_id,
                leetcode_contest
            )

            if participated:
                leetcode_status = "✅ Participated"
            else:
                leetcode_status = "❌ Did not participate"

        except Exception as error:
            leetcode_status = f"⚠️ {error}"

    else:
        leetcode_status = "⚠️ ID not provided"

    leetcode_history.append({
        "Roll No": student["Roll No"],
        "Name": name,
        "Section": student["Section"],
        "LeetCode ID": leetcode_id,
        "Contest": leetcode_contest,
        "Participation": leetcode_status
    })


    # -------------------------
    # Display
    # -------------------------

    print(
        f"{student['Roll No']} | "
        f"{name} | "
        f"CodeChef: {codechef_status} | "
        f"LeetCode: {leetcode_status}"
    )


    # -------------------------
    # Store result
    # -------------------------

    results.append({
        "Roll No": student["Roll No"],
        "Name": name,
        "Section": student["Section"],
        "CodeChef ID": codechef_id,
        "LeetCode ID": leetcode_id,
        "CodeChef Participation": codechef_status,
        "LeetCode Participation": leetcode_status
    })


write_results(results)

save_codechef_history(codechef_history)
save_leetcode_history(leetcode_history)

# Generate statistics
statistics_results = calculate_statistics()

write_statistics(statistics_results)

print("\nResults successfully written to Google Sheets.")
print("Statistics updated successfully.")