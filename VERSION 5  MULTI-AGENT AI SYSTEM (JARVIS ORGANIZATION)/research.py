import urllib.parse
import requests
from bs4 import BeautifulSoup


def research_agent(query):
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        snippets = []

        # Try Google's result snippet divs (most reliable selectors)
        for tag in soup.select("div.BNeawe, div.VwiC3b, span.aCOpRe"):
            text = tag.get_text(separator=" ").strip()
            if text and len(text) > 40 and text not in snippets:
                snippets.append(text)
            if len(snippets) >= 4:
                break

        # Fallback: grab all visible paragraph text
        if not snippets:
            for p in soup.find_all("p"):
                text = p.get_text(separator=" ").strip()
                if len(text) > 40:
                    snippets.append(text)
                if len(snippets) >= 3:
                    break

        if snippets:
            return "\n\n".join(snippets[:4])
        return f"No rich snippets found. Page title: {soup.title.text if soup.title else 'N/A'}"

    except Exception as e:
        return f"Research error: {e}"
