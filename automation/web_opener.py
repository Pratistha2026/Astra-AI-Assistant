import webbrowser

websites = {
    # Search & Google services
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "google maps": "https://maps.google.com",
    "maps": "https://maps.google.com",
    "google drive": "https://drive.google.com",
    "drive": "https://drive.google.com",
    "google photos": "https://photos.google.com",
    "google docs": "https://docs.google.com",
    "google sheets": "https://sheets.google.com",
    "google calendar": "https://calendar.google.com",
    "calendar": "https://calendar.google.com",
    "google translate": "https://translate.google.com",
    "translate": "https://translate.google.com",

    # Social media
    "youtube": "https://www.youtube.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "x": "https://www.twitter.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "pinterest": "https://www.pinterest.com",
    "snapchat": "https://web.snapchat.com",
    "tiktok": "https://www.tiktok.com",
    "discord": "https://discord.com/app",
    "whatsapp web": "https://web.whatsapp.com",
    "telegram": "https://web.telegram.org",

    # Developer / tech
    "github": "https://www.github.com",
    "gitlab": "https://www.gitlab.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
    "leetcode": "https://leetcode.com",
    "hackerrank": "https://www.hackerrank.com",
    "geeksforgeeks": "https://www.geeksforgeeks.org",
    "chatgpt": "https://chat.openai.com",
    "claude": "https://claude.ai",
    "kaggle": "https://www.kaggle.com",
    "codeforces": "https://codeforces.com",
    "replit": "https://replit.com",
    "npm": "https://www.npmjs.com",

    # Entertainment / streaming
    "netflix": "https://www.netflix.com",
    "prime video": "https://www.primevideo.com",
    "hotstar": "https://www.hotstar.com",
    "spotify web": "https://open.spotify.com",
    "twitch": "https://www.twitch.tv",

    # Shopping
    "amazon": "https://www.amazon.com",
    "flipkart": "https://www.flipkart.com",
    "ebay": "https://www.ebay.com",
    "myntra": "https://www.myntra.com",

    # News / reference
    "wikipedia": "https://www.wikipedia.org",
    "bbc news": "https://www.bbc.com/news",
    "times of india": "https://timesofindia.indiatimes.com",

    # Productivity / misc
    "notion": "https://www.notion.so",
    "canva": "https://www.canva.com",
    "zoom": "https://zoom.us",
    "outlook web": "https://outlook.com",
}

def open_website(site_name):
    site_name = site_name.lower().strip()

    if site_name in websites:
        webbrowser.open(websites[site_name])
        return True

    return False