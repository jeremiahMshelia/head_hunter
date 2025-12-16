# HEADHUNTER Bot 🚀

An intelligent, interactive Discord Job Agent that finds tailored Design Engineering roles, analyzes them with Groq LLM, and drafts context-aware cover letters.

## ✨ Features

- **Multi-Source Scraping**: Monitors Dribbble, Himalayas, and 10+ RSS Feeds.
- **Smart Analysis (Groq/Llama3)**: 
    - Analyzes **Company Vibe** and **Pain Points**.
    - Matches against your **Specific Projects** (Visual Vault, Mercer & Co, etc.).
- **Interactive Discord Bot**:
    - **Notifications**: Rich Embeds with Match Score, Vibe, and Reasoning.
    - **Refinement**: Reply to any job instanly to rewrite the cover letter.
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

1. Create a **Web Service** on Render connected to this repo.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. **Environment Variables**: Add `GROQ_API_KEY` and `DISCORD_TOKEN`.

### ⚠️ Critical Checks
1. **Discord Portal**: Go to [Discord Developer Portal](https://discord.com/developers/applications) -> Your Bot -> **Bot** Tab -> Enable **MESSAGE CONTENT INTENT**. (Required for the bot to read your commands).
2. **Free Tier**: If using Render Free Tier, the bot will sleep after 15 mins of inactivity. Use a free service like **UptimeRobot** to ping `https://your-bot.onrender.com` every 5 minutes to keep it alive.

## 🕹 Commands
- `!start`: Activate 30-min auto-scan.
- `!scan`: Manual scan (New jobs only).
- `!scan force`: **Manual Force Scan** (Re-analyze EVERYTHING on the board - uses more credits).
- `!stop`: Stop auto-scan.

## 🧠 Customization
Edit `config.py` to update your `MY_PROFILE` and `MY_PROJECTS`. The AI reads this file to generate its "Reasoning".
