import json
import os
from datetime import date

DATA_FILE = "cp_tracker_data.json"


def load_data():
    """Load saved records. Create an empty tracker if no data file exists."""
    if not os.path.exists(DATA_FILE):
        return {"problems": [], "contests": [], "daily_logs": []}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {
            "problems": data.get("problems", []),
            "contests": data.get("contests", []),
            "daily_logs": data.get("daily_logs", [])
        }
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with an empty tracker.")
        return {"problems": [], "contests": [], "daily_logs": []}


def save_data(data):
    """Save all tracker records to a JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_integer(prompt, minimum=0):
    """Read and validate an integer from the user."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter a number greater than or equal to {minimum}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def add_problem(data):
    print("\n--- Add Solved Problem ---")
    name = input("Problem name: ").strip()
    platform = input("Platform (Codeforces/AtCoder/etc.): ").strip()
    topic = input("Topic (DP/Greedy/Graphs/etc.): ").strip()
    rating = get_integer("Problem difficulty/rating: ")

    if not name or not platform or not topic:
        print("Name, platform and topic cannot be empty.")
        return

    data["problems"].append({
        "name": name,
        "platform": platform,
        "topic": topic,
        "rating": rating,
        "date": date.today().isoformat()
    })
    save_data(data)
    print("Problem added successfully!")


def add_contest(data):
    print("\n--- Add Contest ---")
    name = input("Contest name: ").strip()
    platform = input("Platform: ").strip()
    old_rating = get_integer("Rating before contest: ")
    new_rating = get_integer("Rating after contest: ")

    if not name or not platform:
        print("Contest name and platform cannot be empty.")
        return

    data["contests"].append({
        "name": name,
        "platform": platform,
        "old_rating": old_rating,
        "new_rating": new_rating,
        "change": new_rating - old_rating,
        "date": date.today().isoformat()
    })
    save_data(data)
    print("Contest record added successfully!")


def add_daily_log(data):
    print("\n--- Daily Practice Tracker ---")
    hours = get_integer("Practice hours today (whole number): ")
    completed = input("Did you complete your planned routine? (y/n): ").strip().lower()

    if completed not in ("y", "n"):
        print("Please enter y or n.")
        return

    data["daily_logs"].append({
        "date": date.today().isoformat(),
        "hours": hours,
        "completed": completed == "y"
    })
    save_data(data)
    print("Daily log saved successfully!")


def view_problems(data):
    print("\n--- Solved Problems ---")
    if not data["problems"]:
        print("No problems recorded yet.")
        return

    for number, problem in enumerate(data["problems"], start=1):
        print(
            f"{number}. {problem['name']} | {problem['platform']} | "
            f"{problem['topic']} | Rating: {problem['rating']} | {problem['date']}"
        )


def view_statistics(data):
    print("\n--- Performance Statistics ---")
    problems = data["problems"]
    contests = data["contests"]
    logs = data["daily_logs"]

    print(f"Total problems solved: {len(problems)}")
    print(f"Total contests attended: {len(contests)}")
    print(f"Practice days recorded: {len(logs)}")

    if problems:
        topic_counts = {}
        for problem in problems:
            topic = problem["topic"].title()
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        print("\nProblems solved by topic:")
        for topic, count in sorted(topic_counts.items()):
            print(f"- {topic}: {count}")

        strongest = max(topic_counts, key=topic_counts.get)
        least_practiced = min(topic_counts, key=topic_counts.get)
        print(f"Most practiced topic: {strongest}")
        print(f"Least represented topic: {least_practiced}")

        average_rating = sum(p["rating"] for p in problems) / len(problems)
        print(f"Average problem rating: {average_rating:.1f}")
    else:
        print("Add solved problems to see topic statistics.")

    if contests:
        latest = contests[-1]
        print(
            f"\nLatest recorded rating: {latest['new_rating']} "
            f"({latest['change']:+d} in {latest['name']})"
        )
        total_change = sum(contest["change"] for contest in contests)
        print(f"Total rating change across recorded contests: {total_change:+d}")
    else:
        print("No contest rating records available.")

    if logs:
        total_hours = sum(log["hours"] for log in logs)
        completed_days = sum(1 for log in logs if log["completed"])
        print(f"\nTotal practice hours: {total_hours}")
        print(f"Days routine completed: {completed_days}/{len(logs)}")
    else:
        print("No daily practice records available.")


def main():
    data = load_data()

    while True:
        print("\n========== COMPETITIVE PROGRAMMING TRACKER ==========")
        print("1. Add solved problem")
        print("2. Add contest record")
        print("3. Add daily practice log")
        print("4. View solved problems")
        print("5. View performance statistics")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_problem(data)
        elif choice == "2":
            add_contest(data)
        elif choice == "3":
            add_daily_log(data)
        elif choice == "4":
            view_problems(data)
        elif choice == "5":
            view_statistics(data)
        elif choice == "6":
            save_data(data)
            print("Thank you for using Competitive Programming Tracker!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()
