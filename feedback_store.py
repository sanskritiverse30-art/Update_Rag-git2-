import csv
import os
import datetime


class FeedbackStore:

    def __init__(self, file_path="report.csv"):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "question",
                    "answer",
                    "helpful"
                ])

    # -----------------------
    # LOG USAGE (optional)
    # -----------------------
    def log(self, question, answer, sources, feedback):
        # optional: you can ignore sources or extend later
        pass

    # -----------------------
    # ADD FEEDBACK
    # -----------------------
    def add_feedback(self, question, answer, helpful):

        timestamp = datetime.datetime.now().isoformat()

        with open(self.file_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                question,
                answer,
                str(helpful)   # IMPORTANT: store as string
            ])

    # -----------------------
    # STATS (FIXED)
    # -----------------------
    def get_stats(self):

        total = 0
        positive = 0

        if not os.path.exists(self.file_path):
            return {
                "total_queries": 0,
                "helpfulness_rate": 0
            }

        with open(self.file_path, mode="r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                total += 1

                if row.get("helpful", "False") == "True":
                    positive += 1

        rate = (positive / total * 100) if total > 0 else 0

        return {
            "total_queries": total,
            "helpfulness_rate": round(rate, 2)
        }