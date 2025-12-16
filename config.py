import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Time Filter
MAX_JOB_AGE_DAYS = 3

# Data Sources
RSS_FEEDS = [
    "https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-design-jobs.rss",
    "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    "https://remoteok.com/remote-react-jobs.rss",
    "https://hnrss.org/whoishiring/jobs?q=Remote",
    "https://remotive.com/remote-jobs/frontend/feed",
    "https://remotive.com/remote-jobs/design/feed",
    "https://jobspresso.co/remote-design-jobs/feed/",
    "https://jobspresso.co/remote-software-jobs/feed/",
    "https://authenticjobs.com/feed/",
]

# Keywords
INCLUDE_KEYWORDS = ["Senior", "Lead", "Frontend", "Creative", "Design Engineer", "Creative Developer", "Next", "React", "UI Engineer", "UX Engineer", "Creative Technologist", "Interactive"]
EXCLUDE_KEYWORDS = ["Java", "C#", ".NET", "DevOps", "Ruby", "Manager", "Cloud"]

# Persona & Projects
MY_PROFILE = """
I am Jeremiah James, a Design Engineer and Founder of Jeti Labs (Jeremiah's Tech Interface) - www.jetilabs.xyz.
**The USP:** I bridge the gap between UI Design (Figma) and Engineering (Code). I don't just implement designs; I craft interactions.
**The Stack:** Next.js 16 (App Router/Turbopack), TypeScript, Tailwind CSS, Supabase.
**The Secret Sauce:** Advanced Motion (GSAP ScrollTrigger, Flip, Framer Motion) and WebGL.
"""

MY_PROJECTS = {
    "Visual Vault": """
    **Visual Vault (Product Engineering)** - *https://www.visualvault.xyz*
    - *Type:* Complex Web Application (Local-first).
    - *Stack:* Next.js, Framer Motion, Zustand (State Management), IndexedDB.
    - *Key Features:* Infinite Canvas with pan/zoom, Drag & Drop uploads, Multi-selection/grouping, Persistent local storage suitable for heavy workflows.
    - *Use Case:* Use for "Product Engineer", "Full Stack", "React Specialist" roles. Proof of complex UI logic.
    """,
    
    "Little Qalb": """
    **Little Qalb (Product Engineering)** - *https://www.littleqalb.com*
    - *Type:* Hybrid PWA (React) for Islamic families.
    - *Stack:* React, PWA (Offline capable), Tablet-first design.
    - *Key Features:* "Child Gate" security logic, Neurodivergent-friendly settings (low stim), Responsive Audio player, Splash screen & onboarding flow.
    - *Use Case:* Use for "App Developer", "Product", "User-Centric" roles. Proof of empathy/accessibility.
    """,
    
    "Mercer & Co": """
    **Mercer & Co (Creative Frontend)** - *https://mercer-co.vercel.app*
    - *Type:* Luxury Real Estate Concept.
    - *Stack:* Next.js, GSAP (GreenSock), Lenis Scroll.
    - *Key Features:* Cinematic "Keyhole" Preloader, Advanced scroll-triggered reveals, Glassmorphism UI, Custom full-screen mobile menu.
    - *Use Case:* Use for "Creative Developer", "Awwwards", "Luxury/Brand" roles. Proof of motion/polish.
    """,
    
    "Veridian": """
    **Veridian (Creative Frontend)** - *https://veridan.vercel.app*
    - *Type:* Architecture Studio Showcase.
    - *Stack:* Next.js (App Router), TypeScript, GSAP, Vera AI (DeepSeek R1 integration).
    - *Key Features:* Cinematic "Liquid Glass" UI, Story-driven scrolling, Integrated AI Chatbot (Vera) for visitor Q&A.
    - *Use Case:* Use for "Design Engineer", "Interactive", "AI Interface" roles. Proof of modern tech/AI integration.
    """
}
