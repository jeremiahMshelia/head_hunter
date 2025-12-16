import discord
from discord.ext import tasks
from config import DISCORD_TOKEN
from ai_agent import refine_cover_letter
from scrapers import scan_all, SEEN_JOBS

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

TARGET_CHANNEL_ID = None
FIRST_RUN_CHECKED = False

async def send_discord_notification(job_data: dict, job_url: str, title: str):
    """Callback function used by scrapers to send alerts."""
    global TARGET_CHANNEL_ID
    if not TARGET_CHANNEL_ID: return

    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not channel: return
    
    score = job_data.get("match_score", 0)
    color = 0x00FF00 if score > 90 else 0x0099FF
    
    company = job_data.get('company', 'Unknown')
    vibe = job_data.get('company_vibe', 'Unknown')
    
    embed = discord.Embed(
        title=f"🎯 Lead: {company}",
        url=job_url,
        color=color
    )
    embed.add_field(name="Role", value=title, inline=True)
    embed.add_field(name="Match Score", value=f"{score}%", inline=True)
    embed.add_field(name="Vibe", value=vibe, inline=True)
    
    # Reasoning / Insight
    pain_points = job_data.get('key_pain_points', [])
    if isinstance(pain_points, list):
        pain_points_str = "\n".join([f"• {p}" for p in pain_points])
    else:
        pain_points_str = str(pain_points)
        
    reasoning = job_data.get('reasoning', 'No specific reasoning provided.')
    
    embed.add_field(name="💡 Why it Matched", value=f"**Strategy:** {reasoning}\n**Pain Points:**\n{pain_points_str}", inline=False)
    
    cover_letter = job_data.get('cover_letter', 'No letter generated')
    if len(cover_letter) > 1000: cover_letter = cover_letter[:1000] + "..."
        
    embed.add_field(name="Cover Letter Draft", value=f"```\n{cover_letter}\n```", inline=False)
    embed.set_footer(text="Reply / Create Thread to refine!")
    
    try:
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Discord Send Error: {e}")

@tasks.loop(minutes=30)
async def scheduled_scan():
    await scan_all(send_discord_notification)

@bot.event
async def on_ready():
    global FIRST_RUN_CHECKED
    print(f'Bot {bot.user} is ready.')
    
    if not FIRST_RUN_CHECKED:
        FIRST_RUN_CHECKED = True
        # If the seen list is empty, this implies a fresh install or wiped memory.
        # We run a "Silent Calibration" to mark everything current as seen without spamming.
        if len(SEEN_JOBS) == 0:
            print("Detected Fresh Install (Empty Memory). Running Silent Calibration...")
            await scan_all(send_discord_notification, ignore_analysis=True)
            print("Calibration Complete. Memory hydrated.")

@bot.event
async def on_message(message):
    global TARGET_CHANNEL_ID
    if message.author == bot.user: return

    # Commands
    if message.content.startswith('!start'):
        TARGET_CHANNEL_ID = message.channel.id
        await message.channel.send("🚀 HeadHunter Active! Scanning every 30m.")
        if not scheduled_scan.is_running(): scheduled_scan.start()
        return

    if message.content.startswith('!stop'):
        if scheduled_scan.is_running():
            scheduled_scan.cancel()
            await message.channel.send("🛑 Stopped.")
        else:
            await message.channel.send("Not running.")
        return

    if message.content.startswith('!scan'):
        TARGET_CHANNEL_ID = message.channel.id
        
        is_force = "force" in message.content.lower()
        if is_force:
            await message.channel.send("🕵️ Manual Force Scan (Checking EVERYTHING)...")
            await scan_all(send_discord_notification, force_rescan=True)
        else:
            await message.channel.send("🕵️ Manual Scan (New items only)...")
            await scan_all(send_discord_notification)
        return

    # Refinement Logic
    original_msg = None
    if message.reference:
        try:
             original_msg = await message.channel.fetch_message(message.reference.message_id)
        except: pass
    elif isinstance(message.channel, discord.Thread):
        try:
            original_msg = await message.channel.parent.fetch_message(message.channel.id)
        except: pass

    if original_msg and (original_msg.author == bot.user or original_msg.webhook_id) and original_msg.embeds:
        try:
             embed = original_msg.embeds[0]
             original_text = ""
             for field in embed.fields:
                 if "Cover Letter" in field.name:
                     original_text = field.value.replace("```", "")
             
             if not original_text: original_text = "No context."

             async with message.channel.typing():
                 refined = await refine_cover_letter(original_text, message.content)
             
             await message.reply(f"Sure:\n\n```\n{refined}\n```")
        except Exception as e:
             print(f"Refine Error: {e}")

def run_bot():
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("No Discord Token found in environment.")
