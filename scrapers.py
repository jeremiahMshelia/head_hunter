import httpx
from bs4 import BeautifulSoup
from utils import is_potentially_relevant, is_recent, load_seen_jobs, save_seen_jobs
from config import INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS, RSS_FEEDS, MAX_JOB_AGE_DAYS
from ai_agent import analyze_job
import feedparser

# Global Seen Jobs Set (managed via utils)
SEEN_JOBS = load_seen_jobs()

async def scrape_dribbble():
    print("Scraping Dribbble Jobs...")
    url = "https://dribbble.com/jobs"
    jobs = []
    
    async with httpx.AsyncClient() as client:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Dribbble scrape failed: {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            job_links = soup.find_all('a', class_='job-board-job-link') 
            
            if not job_links:
                 all_links = soup.find_all('a', href=True)
                 job_links = [a for a in all_links if '/jobs/' in a['href'] and 'source=index' in a['href']]

            for link_tag in job_links:
                try:
                    href = link_tag['href']
                    full_link = f"https://dribbble.com{href}" if href.startswith('/') else href
                    
                    title_div = link_tag.find('div', class_='job-board-job-title')
                    title = title_div.get_text(strip=True) if title_div else "Unknown Title"
                    
                    company_div = link_tag.find('div', class_='job-board-job-company')
                    company = company_div.get_text(strip=True) if company_div else "Unknown Company"
                    
                    # Time Logic
                    time_div = link_tag.find('div', class_='job-board-job-posted')
                    if not time_div:
                         time_div = link_tag.find('span', string=lambda x: x and ("ago" in x or "Posted" in x))
                    time_text = time_div.get_text(strip=True) if time_div else "No Date"
                    
                    if "month" in time_text or "year" in time_text: continue
                    if "day" in time_text:
                        try:
                            days_ago = int(''.join(filter(str.isdigit, time_text)))
                            if days_ago > MAX_JOB_AGE_DAYS: continue
                        except: pass 

                    jobs.append({
                        'id': full_link,
                        'link': full_link,
                        'title': f"{company}: {title}",
                        'description': f"Role at {company}. View on Dribbble: {full_link}",
                        'is_dribbble': True
                    })
                except Exception: continue
            print(f"Dribbble: Found {len(jobs)} potential fresh jobs.")
        except Exception as e:
            print(f"Error scraping Dribbble: {e}")
            
    return jobs

async def scrape_himalayas():
    print("Scraping Himalayas...")
    base_urls = [
        "https://himalayas.app/jobs/design",
        "https://himalayas.app/jobs/software-engineering?skills=frontend"
    ]
    jobs = []
    
    async with httpx.AsyncClient() as client:
        for url in base_urls:
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
                response = await client.get(url, headers=headers, follow_redirects=True)
                if response.status_code != 200: continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                candidate_links = soup.find_all('a', href=True)
                
                for link in candidate_links:
                    href = link['href']
                    if '/companies/' not in href or '/jobs/' not in href: continue
                    full_link = f"https://himalayas.app{href}"
                    text = link.get_text(strip=True)
                    if not text: continue

                    if is_potentially_relevant(text, INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS):
                        try:
                            company_slug = href.split('/companies/')[1].split('/')[0]
                            company_name = company_slug.replace('-', ' ').title()
                        except: company_name = "Himalayas Job"

                        jobs.append({
                            'id': full_link,
                            'link': full_link,
                            'title': f"{company_name}: {text}",
                            'description': f"Role found on Himalayas: {text}. Link: {full_link}",
                            'is_himalayas': True
                        })
            except Exception: pass
    print(f"Himalayas: Found {len(jobs)} relevant jobs.")
    return jobs

async def scan_all(notify_callback, ignore_analysis=False, force_rescan=False):
    """Orchestrates all scrapers. 
       - ignore_analysis=True: Silent learning (Startup).
       - force_rescan=True: Re-analyze everything (Manual Override).
    """
    mode_str = "Calibration" if ignore_analysis else ("FORCED" if force_rescan else "Normal")
    print(f"Starting scan_all (Mode: {mode_str})...")
    
    # helper to process result
    async def process_job(job_title, job_desc, job_link, job_id, source):
        # If force_rescan is True, we proceed EVEN IF it's in SEEN_JOBS
        if (job_id in SEEN_JOBS) and (not force_rescan): 
            return
            
        SEEN_JOBS.add(job_id)
        save_seen_jobs(SEEN_JOBS)
        
        if ignore_analysis:
            return

        if is_potentially_relevant(job_title, INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS):
            print(f"[{source}] Analyzing: {job_title}")
            analysis = await analyze_job(job_title, job_desc)
            if analysis and analysis.get('match_score', 0) >= 85:
                print(f"MATCH: {analysis['match_score']}")
                # If forcing rescan, maybe add a tag to title?
                display_title = f"[Rescan] {job_title}" if force_rescan else job_title
                await notify_callback(analysis, job_link, display_title)

    # Dribbble
    dribbble_jobs = await scrape_dribbble()
    for job in dribbble_jobs:
        await process_job(job['title'], job['description'], job['link'], job['id'], "Dribbble")

    # Himalayas
    himalayas_jobs = await scrape_himalayas()
    for job in himalayas_jobs:
        await process_job(job['title'], job['description'], job['link'], job['id'], "Himalayas")

    # RSS
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                job_id = entry.get('id', entry.get('link'))
                if not is_recent(entry): continue
                
                title = entry.get('title', 'No Title')
                link = entry.get('link', '')
                desc = entry.get('description', '') or entry.get('summary', '')
                
                await process_job(title, desc, link, job_id, "RSS")
        except Exception as e:
            print(f"RSS Error {feed_url}: {e}")
            
    print("Scan complete.")
