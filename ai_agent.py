from groq import Groq
from config import GROQ_API_KEY, MY_PROFILE, MY_PROJECTS
import json

client = Groq(api_key=GROQ_API_KEY)

async def analyze_job(title: str, description: str):
    """Analyzes a job to see if it Matches Jerry's profile with Deep Reasoning."""
    prompt = f"""
    You are an Expert Design Recruiter.
    
    CANDIDATE:
    {MY_PROFILE}
    
    PROJECTS (Evidence Interaction):
    {json.dumps(MY_PROJECTS, indent=2)}
    
    JOB TITLE: {title}
    JOB DESCRIPTION: {description[:4000]}
    
    PHASE 1: ANALYSIS
    - Identify the Company Vibe (Corporate / Startup / Creative Studio).
    - Identify the top 3 "Pain Points".
    - Select the ONE BEST PROJECT from my list to mention as proof. 
      (e.g. if they want Motion, use Mercer. If they want App complexity, use Visual Vault).
    
    PHASE 2: DRAFTING (If Match > 80)
    - Tone Strategy: Adapt to Vibe.
    - Structure:
      - Hook: Address a pain point.
      - Evidence: deeply describe the selected project ({MY_PROJECTS['Visual Vault']} OR {MY_PROJECTS['Mercer & Co']}) to prove competence.
        DON'T just drop the name. Say "For example, in Visual Vault, I built a..."
    - Rules:
      - Link: https://www.jetilabs.xyz
      - NO Fluff ("passionate", "thrilled").
    
    OUTPUT JSON ONLY:
    {{
        "match_score": number,
        "is_match": boolean,
        "company": "string",
        "company_vibe": "string",
        "key_pain_points": ["string"],
        "selected_project": "string",
        "reasoning": "string",
        "cover_letter": "string"
    }}
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful automation assistant that outputs only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, 
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error analyzing job {title}: {e}")
        return None

async def refine_cover_letter(original_text: str, instruction: str):
    """Refines the text based on user instruction."""
    prompt = f"""
    You are my Career Agent (Jerry, Design Engineer).
    
    MY PROFILE & PROJECTS:
    {MY_PROFILE}
    {json.dumps(MY_PROJECTS, indent=2)}
    - Portfolio: https://www.jetilabs.xyz
    
    ORIGINAL DRAFT:
    {original_text}
    
    USER INSTRUCTION:
    {instruction}
    
    CRITICAL STYLE RULES:
    1. Context Aware: If the user asks to "Focus on Motion", switch the story to Mercer & Co detailed description.
    2. If the user asks for "App Logic", switch story to Visual Vault (Zustand/Infinite Canvas).
    3. NO FLUFF. Direct and punchy.
    4. Link: https://www.jetilabs.xyz

    Output ONLY the rewritten text.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                 {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error refining: {e}"
