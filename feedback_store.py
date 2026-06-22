import json
import os
import pandas as pd
from datetime import datetime


class FeedbackStore:
    def __init__(self, path="feedback.jsonl"):
        self.path = path

        if not os.path.exists(self.path):
            open(self.path, "w").close()

    def log(self, question, answer, sources, feedback):
        record = {
            "question": question,
            "answer": answer,
            "sources": sources,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }

        with open(self.path, "a") as f:
            f.write(json.dumps(record) + "\n")

    def get_stats(self):
        records = []

        with open(self.path, "r") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))

        total = len(records)
        helpful = sum(1 for r in records if r["feedback"] == "y")
        not_helpful = total - helpful

        return {
            "total_queries": total,
            "helpful": helpful,
            "not_helpful": not_helpful,
            "helpfulness_rate": round((helpful / total) * 100, 2) if total else 0
        }

    def export_csv(self):
        records = []

        with open(self.path, "r") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))

        df = pd.DataFrame(records)

        output = "report.csv"
        df.to_csv(output, index=False)

        return output