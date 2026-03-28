import os
from datetime import datetime


class AuditLogger:
    def __init__(self, file_path="data/audit.log"):
        self.file_path = file_path

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def log(self, action, details):
        """
        action: string (e.g., ASSIGN_ROLE, CREATE_USER)
        details: dictionary (key-value info)
        """

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Convert details dict → key=value format
        details_str = " | ".join([f"{k}={v}" for k, v in details.items()])

        # Final log line
        log_line = f"[{timestamp}] {action} | {details_str}\n"

        # Write to file
        with open(self.file_path, "a") as f:
            f.write(log_line)