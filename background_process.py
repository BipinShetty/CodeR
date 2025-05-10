import threading
import time
from memory_store import archive_old_issues

# This function sets up a background job that periodically archives old issues.
# It's useful for simulating a production-like cleanup mechanism.
def start_archiver():
    def archive_job():
        while True:
            # Archive any issues older than the threshold (default is 30 days)
            archive_old_issues()
            # Sleep for an hour before checking again
            time.sleep(3600)  # Run every hour

    # Run the archive job in a separate daemon thread so it doesn't block shutdown
    threading.Thread(target=archive_job, daemon=True).start()