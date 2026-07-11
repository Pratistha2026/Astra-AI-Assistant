import requests

# Replace with your real Render URL once deployed, e.g:
# "https://astra-backend-xxxx.onrender.com/ask"
BACKEND_URL = "https://astra-backend-93sl.onrender.com/ask"


def ask_ai(question):
    """
    Sends a question to Astra's backend server and returns
    (answer_text, page_url_or_None). Never touches an API key directly -
    the backend holds that. Handles errors safely so Astra never crashes.
    """
    try:
        response = requests.post(
            BACKEND_URL,
            json={"question": question},
            timeout=45,  # first request after idle can be slow on free hosting
        )

        if response.status_code == 429:
            return "I'm getting a lot of questions right now, please try again in a bit.", None

        response.raise_for_status()
        data = response.json()
        return data.get("answer", "Sorry, I didn't get a clear answer."), data.get("page_url")

    except requests.exceptions.RequestException as e:
        print(f"Backend connection error: {e}")
        return "Sorry, I can't reach my AI brain right now. Please check your internet connection.", None