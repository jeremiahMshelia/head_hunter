from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import os
from bot import bot, DISCORD_TOKEN

# Render requires a web server to keep the service alive.
# We run FastAPI on the main thread and the Discord Bot as a background task.

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch Discord Bot
    loop = asyncio.get_event_loop()
    if DISCORD_TOKEN:
        print("Starting Discord Bot task...")
        # create_task schedules the coroutine on the loop
        asyncio.create_task(bot.start(DISCORD_TOKEN))
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
@app.head("/")
async def home():
    return {
        "status": "HeadHunter Active", 
        "bot_user": str(bot.user) if bot.user else "Starting..."
    }

if __name__ == "__main__":
    import uvicorn
    # Verify port for Render (defaults to 10000)
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
