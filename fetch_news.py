import feedparser

def fetch_news(rss_url="https://news.google.com/rss?topic", limit=1):
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        print("No news entries found.")
        return [], [], [], []

    news_data = [
        (
            entry.title.split(" - ")[0].strip(),
            entry.title.split(" - ")[-1].strip(),
            entry.link,
            entry.get("published", "No date available")
        )
        for entry in feed.entries[:limit]
    ]

    titles, sources, links, published_dates = zip(*news_data)
    return list(sources), list(titles), list(links), list(published_dates)