# HEADHUNTER Bot 🚀

An intelligent, interactive Discord Job Agent that finds tailored Design Engineering roles, analyzes them with Groq LLM, and drafts context-aware cover letters.

## ✨ Features

- **Multi-Source Scraping**: Monitors Dribbble, Himalayas, and 10+ RSS Feeds.
- **Smart Analysis (Groq/Llama3)**: 
    - Analyzes **Company Vibe** and **Pain Points**.
    - Matches against your **Specific Projects** (Visual Vault, Mercer & Co, etc.).
- **Source Hunter Strategy** 🕵️‍♀️:
    - Automatically bypasses aggregator paywalls (e.g., WeWorkRemotely $3 fees).
    - **Hybrid Logic**:
        - **Phase 1 (Sniper)**: Guesses direct ATS links (Ashby, Greenhouse, Lever).
        - **Phase 2 (Net)**: Falls back to DuckDuckGo Search to find the real careers page.
    - Delivers **Direct Application Links** to Discord.
- **Interactive Discord Bot**:
    - **Notifications**: Rich Embeds with Match Score, Vibe, and Reasoning.
    - **Refinement**: Reply to any job instantly to rewrite the cover letter.
    - **Commands**: `!scan`, `!scan force`, `!start`, `!stop`.

## 🛠 Tech Stack

- **Python** (FastAPI, Discord.py)
- **AI**: Groq API (Llama-3.3-70b)
- **Deployment**: Render (Web Service)

## ⚡ Quick Setup (Local)

1. **Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Env Vars**: Create `.env`
   ```env
   GROQ_API_KEY=gsk_...
   DISCORD_TOKEN=...
   ```
3. **Run**:
   ```bash
   uvicorn main:app --reload
   ```

## 🚀 Deployment (Render)

1. **Push to GitHub**: Commit your code and push it to a new GitHub repository.
2. **Create Web Service**:
   - Go to [Render Dashboard](https://dashboard.render.com).
   - Click **New +** -> **Web Service**.
   - Connect your GitHub repo.
3. **Configure Settings**:
   - **Name**: `head-hunter-bot`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. **Environment Variables** (Scroll down to "Environment"):
   - Key: `GROQ_API_KEY` | Value: `gsk_...`
   - Key: `DISCORD_TOKEN` | Value: `...`
5. **Deploy**: Click **Create Web Service**.

### ⚠️ Keeping it Alive (Free Tier)
Render's free tier spins down after 15 mins of inactivity. To keep your bot 24/7:
1. Copy your Render URL (e.g., `https://head-hunter.onrender.com`).
2. Set up a free monitor on [UptimeRobot](https://uptimerobot.com).
3. Create a **HTTP Monitor** that pings your URL every 5 minutes.
This keeps the web server awake, which keeps the Bot alive!

## 🕹 Commands
- `!start`: Activate 30-min auto-scan.
- `!scan`: Manual scan (New jobs only).
- `!scan force`: **Manual Force Scan** (Re-analyze EVERYTHING on the board - uses more credits).
- `!stop`: Stop auto-scan.

## 🧠 Customization
Edit `config.py` to update your `MY_PROFILE` and `MY_PROJECTS`. The AI reads this file to generate its "Reasoning".
