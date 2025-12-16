import json
import os
from datetime import datetime, timezone
from time import mktime
from config import MAX_JOB_AGE_DAYS

SEEN_JOBS_FILE = "seen_jobs.json"

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        try:
            with open(SEEN_JOBS_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_seen_jobs(seen_jobs_set):
    try:
        with open(SEEN_JOBS_FILE, "w") as f:
            json.dump(list(seen_jobs_set), f)
    except Exception as e:
        print(f"Error saving seen jobs: {e}")

def is_potentially_relevant(title: str, include_keywords: list, exclude_keywords: list) -> bool:
    title_lower = title.lower()
    for bad in exclude_keywords:
        if bad.lower() in title_lower:
            return False
    for good in include_keywords:
        if good.lower() in title_lower:
            return True
    return False

def is_recent(entry) -> bool:
    """Checks if the RSS entry is recent."""
    try:
        published_time = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_time = datetime.fromtimestamp(mktime(entry.published_parsed))
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            published_time = datetime.fromtimestamp(mktime(entry.updated_parsed))
            
        if published_time:
            if published_time.tzinfo is None:
                published_time = published_time.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            return (now - published_time).days <= MAX_JOB_AGE_DAYS
            
        return True # Default to True if no date found
    except:
        return True
