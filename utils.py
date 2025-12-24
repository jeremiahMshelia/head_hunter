import json
import os
from datetime import datetime, timezone
from time import mktime
from config import MAX_JOB_AGE_DAYS
from duckduckgo_search import DDGS

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

import httpx
from duckduckgo_search import DDGS

async def find_direct_application_link(company: str, title: str) -> str:
    """
    Hybrid Strategy to find the direct ATS link:
    1. Guessing: specific ATS patterns (Lever, Ashby, Greenhouse).
    2. Search: DuckDuckGo Fallback.
    """
    if not company or company == "Unknown":
        return None

    print(f"  🔍 Source Hunting for {company}...")

    # PHASE 1: SMART GUESSING (Fast & Accurate)
    slug = company.lower().replace(" ", "").replace(".", "")
    slug_hyphen = company.lower().replace(" ", "-").replace(".", "")
    candidates = list(set([slug, slug_hyphen]))
    
    # Common ATS patterns for tech startups
    patterns = [
        "https://jobs.ashbyhq.com/{}",
        "https://jobs.lever.co/{}",
        "https://boards.greenhouse.io/{}",
        "https://{}.breezy.hr",
        "https://apply.workable.com/{}"
    ]
    
    async with httpx.AsyncClient(timeout=3.0) as client:
        for c in candidates:
            for pattern in patterns:
                url = pattern.format(c)
                try:
                    resp = await client.head(url, follow_redirects=True)
                    if resp.status_code == 200:
                        print(f"    👉 Guessed ATS: {url}")
                        return url
                except: pass

    # PHASE 2: FALLBACK SEARCH (If guessing fails)
    query = f'{company} careers'
    print(f"    🦆 Guessing failed, trying Search: {query}")
    
    try:
        # backend="html" is often more permissible for bots
        results = DDGS().text(query, max_results=2, backend="html")
        for r in results:
            link = r['href']
            # If it looks like a careers page or ATS, take it
            if "linkedin" in link or "glassdoor" in link or "weworkremotely" in link:
                 continue
            print(f"    👉 Found via Search: {link}")
            return link
    except Exception as e:
        print(f"    ❌ Search Hunt Failed: {e}")
    
    return None
