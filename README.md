# STA Contest Monitor

A Python-based monitoring system for tracking CodeChef and LeetCode
contest participation of students.

The project was created to reduce the manual effort involved in
monitoring 70+ students as a Student Teacher Assistant (STA).

---

## Features

- Collects student CodeChef and LeetCode IDs from Google Forms.
- Reads student data from Google Sheets.
- Removes duplicate student registrations using Roll No.
- Sorts students alphabetically by name.
- Checks participation in a specified CodeChef contest.
- Checks participation in a specified LeetCode contest.
- Maintains separate CodeChef and LeetCode contest histories.
- Prevents duplicate history records.
- Stores contest dates.
- Calculates:
  - CodeChef participation percentage
  - LeetCode participation percentage
  - Overall participation percentage
  - Recent activity
  - Overall student status
- Writes all results back to Google Sheets.
- Provides a one-click `.bat` launcher.

---

## Project Structure

```text
STA-Contest-Monitor/
│
├── main.py
├── google_sheets.py
├── codechef.py
├── leetcode.py
├── stats.py
│
├── Run_Monitor.bat
├── credentials.json
├── .gitignore
└── README.md
