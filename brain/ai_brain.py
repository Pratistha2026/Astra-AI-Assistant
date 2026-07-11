import os
import json
from pathlib import Path
import google.generativeai as genai

CONFIG_DIR = Path(os.getenv("APPDATA", Path.home())) / "Astra"
CONFIG_FILE = CONFIG_DIR / "config.json"

api_key = None
model = None


def load_saved_key():
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text())
            key = data.get("GEMINI_API_KEY", "").strip()
            return key if key else None
        except Exception:
            return None
    return None


def set_api_key(key):
    global api_key, model
    key = key.strip()
    if not key:
        return False

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"GEMINI_API_KEY": key}))

    api_key = key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    return True


def has_api_key():
    return api_key is not None


_saved = load_saved_key()
if _saved:
    set_api_key(_saved)


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
    if not has_api_key():
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
            continue
        cleaned_lines.append(line)

    answer = "\n".join(cleaned_lines).strip()
    return answer, page_url