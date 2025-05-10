import json
from models import Issue
from memory_store import save_issue

# Replay past issue events from a log file.
# Each line in the input file must be a valid JSON representation of an Issue.
# This is useful for restoring state during development or simulating event re-ingestion.
def replay_events(file_path: str):
    with open(file_path) as f:
        for line in f:
            # Parse each line as a JSON object
            data = json.loads(line)

            # Convert the JSON dict to an Issue model instance
            issue = Issue(**data)

            # Save the reconstructed issue into the store
            save_issue(issue)