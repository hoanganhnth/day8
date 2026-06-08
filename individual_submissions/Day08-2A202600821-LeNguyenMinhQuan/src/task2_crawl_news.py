import json
from datetime import datetime
from pathlib import Path
import feedparser
import requests
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_full_article(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        # VNExpress article body is usually in <p class="Normal">
        paragraphs = soup.find_all('p', class_='Normal')
        if paragraphs:
            return "\n\n".join(p.get_text(strip=True) for p in paragraphs)
        # Fallback if class changes
        return "\n\n".join(p.get_text(strip=True) for p in soup.find_all('p'))
    except Exception:
        return ""

def crawl_all():
    rss_url = "https://vnexpress.net/rss/phap-luat.rss"
    feed = feedparser.parse(rss_url)
    
    for i, entry in enumerate(feed.entries[:5], 1):
        full_text = fetch_full_article(entry.link)
        
        # Parse description to extract image and clean text
        desc_soup = BeautifulSoup(entry.description, "html.parser")
        img_tag = desc_soup.find("img")
        img_markdown = f"![Thumbnail]({img_tag['src']})\n\n" if img_tag else ""
        desc_text = desc_soup.get_text(strip=True)
        
        content = img_markdown + desc_text + "\n\n" + full_text
            
        article = {
            "url": entry.link,
            "title": entry.title,
            "date_crawled": getattr(entry, 'published', datetime.now().isoformat()),
            "content_markdown": content
        }
        filename = f"article_{i:02d}.json"
        filepath = DATA_DIR / filename
        filepath.write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Saved full news: {filepath}")

if __name__ == "__main__":
    crawl_all()
