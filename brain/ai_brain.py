import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Warning: GEMINI_API_KEY not found in .env file. AI features will not work.")
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


# =====================================================================
# 🧠 EDIT ME: This is Astra's "personality + teaching style" instruction.
# It runs before every question, so Astra always explains things simply.
# Feel free to rewrite this in your own words - it directly changes how
# Astra talks to you.
# =====================================================================
SYSTEM_STYLE = """
You are Astra, a warm and friendly AI assistant. Answer the user's question
so that a curious 12-year-old could understand it. Follow these rules:

1. Use very simple, everyday words. Avoid jargon. If you must use a technical
   term, explain it in one short phrase right after it.
2. Keep it short: 2-5 sentences for simple questions. Use a tiny real-life
   example or comparison ("like a...", "imagine...") whenever it helps.
3. Be warm and encouraging in tone, never robotic or preachy.
4. If the topic is something the user could learn more about on a reference
   page (like Wikipedia), end your answer with one line in exactly this
   format so the app can turn it into a clickable link:
   PAGE: <topic name>
   Only include this PAGE line for real topics people might want to read
   more about (e.g. science, history, tech, geography). Skip it for
   small talk, jokes, opinions, or simple factual one-liners like time/date.
"""


def ask_ai(question):
    """
    Sends a question to Gemini AI and returns (answer_text, page_url_or_None).
    Handles errors safely so Astra never crashes because of a bad API call.
    """
    if not api_key:
        return "Sorry, my AI brain isn't set up yet. Please add your API key.", None

    try:
        prompt = f"{SYSTEM_STYLE}\n\nUser question: {question}"
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        answer, page_url = _extract_page_link(raw_text)
        return answer, page_url

    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I had trouble thinking of an answer right now.", None


def _extract_page_link(raw_text):
    """
    Looks for a trailing line like:
        PAGE: Machine learning
    Removes it from the spoken/displayed answer and turns it into a
    Wikipedia search URL the GUI can show as a clickable "Learn more" link.
    """
    lines = raw_text.splitlines()
    page_url = None
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("PAGE:"):
            topic = stripped.split(":", 1)[1].strip()
            if topic:
                query = topic.replace(" ", "_")
                page_url = f"https://en.wikipedia.org/wiki/{query}"
            continue  # don't include this line in the spoken answer
        cleaned_lines.append(line)

    answer = "\n".join(cleaned_lines).strip()
    return answer, page_url
