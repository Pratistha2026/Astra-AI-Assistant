import webbrowser
import urllib.parse

def google_search(query):
    query = query.lower().strip()

    if query:
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        webbrowser.open(url)
        return True

    return False