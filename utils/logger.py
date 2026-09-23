from datetime import datetime


class ActivityLogger:
    def __init__(self):
        self.entries = []

    def log(self, agent_name: str, message: str):
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "message": message,
        }
        self.entries.append(entry)
        return entry

    def get_entries(self):
        return self.entries

    def clear(self):
        self.entries = []


activity_logger = ActivityLogger()