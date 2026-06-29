import email.utils
from datetime import datetime, timezone, timedelta
import feedparser
from bs4 import BeautifulSoup
import aiohttp
import asyncio

GLOBAL_RSS_FEEDS = [
    # US & Americas
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "http://rss.cnn.com/rss/edition_world.rss",
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?profile=12000000&id=1000038",
    "http://feeds.washingtonpost.com/rss/world",
    "https://feeds.npr.org/1004/rss.xml",
    "https://www.latimes.com/world-nation/rss2.0.xml",
    "https://rss.cbc.ca/lineup/world.xml",

    # UK & Europe
    "https://www.theguardian.com/world/rss",
    "https://www.ft.com/?format=rss",
    "https://www.telegraph.co.uk/world-news/rss.xml",
    "https://www.independent.co.uk/news/world/rss",
    "https://tass.com/rss/v2.xml",
    "https://www.france24.com/en/rss",
    "https://www.dw.com/en/top-stories/s-9097?maca=en-rss-en-all-1573-rdf",
    "https://english.elpais.com/arc/outboundfeeds/rss/?outputType=xml",
    "https://www.thelocal.se/feeds/rss.xml",
    "https://www.kyivpost.com/feed",

    # Middle East & Africa
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.arabnews.com/rss.xml",
    "https://www.jpost.com/rss/rssfeed.aspx",
    "https://www.timesofisrael.com/feed/",
    "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf",

    # Asia & Oceania
    "https://english.kyodonews.net/rss/news.xml",
    "https://asia.nikkei.com/rss/feed/category/Politics-Economy",
    "https://www.japantimes.co.jp/feed/",
    "https://www.scmp.com/rss/91/feed",
    "https://www.chinadaily.com.cn/rss/world_rss.xml",
    "https://focustaiwan.tw/rss/news/all",
    "https://www.straitstimes.com/news/world/rss.xml",
    "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "https://www.thehindu.com/news/international/feeder/default.rss",
    "https://e.vnexpress.net/rss/news.rss",
    "https://www.thestar.com.my/rss/World",
    "https://www.abc.net.au/news/feed/52278/rss.xml",
    "https://www.smh.com.au/rss/world.xml",
    
    # Latin America (Missing Major Economies added)
    "https://riotimesonline.com/feed/", # Brazil
    "https://mexiconewsdaily.com/feed/", # Mexico
    "https://buenosairesherald.com/feed", # Argentina

    # Europe (Missing Major Economies added)
    "https://www.ansa.it/english/news/news_rss.xml", # Italy ANSA
    "https://nltimes.nl/rss", # Netherlands NL Times
    "https://www.swissinfo.ch/eng/rss/all", # Switzerland

    # Asia & Middle East (Missing Major Economies added)
    "https://en.yna.co.kr/RSS/news.xml", # South Korea Yonhap
    "https://jakartaglobe.id/rss", # Indonesia
    "https://www.dawn.com/feeds/home", # Pakistan
    "https://www.dailysabah.com/rss", # Turkey

    # Global/Orgs
    "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
]

async def fetch_feed(session, url):
    try:
        # Timeout set to 10 seconds per feed so one slow server doesn't hang us
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                text = await response.text()
                return text
    except Exception as e:
        # Silently ignore connection errors to prevent log spam
        pass
    return None

async def fetch_all_feeds_async():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_feed(session, url) for url in GLOBAL_RSS_FEEDS]
        results = await asyncio.gather(*tasks)
        return results

def fetch_latest_news():
    print(f"Fetching from {len(GLOBAL_RSS_FEEDS)} global media sources asynchronously...")
    
    # Try to get existing event loop, otherwise run directly (safe for background threads)
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # In case this is ever run from an already running async loop (FastAPI core)
            raise RuntimeError("Cannot use asyncio.run() inside a running loop.")
    except RuntimeError:
        pass

    xml_results = asyncio.run(fetch_all_feeds_async())
    
    news_items = []
    success_count = 0
    
    for xml in xml_results:
        if not xml:
            continue
            
        success_count += 1
        feed = feedparser.parse(xml)
        # Fetch top 10 from each successful feed to cap around 400-500 max
        for entry in feed.entries[:10]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            published = entry.get("published", "")
            
            try:
                if published:
                    pub_dt = email.utils.parsedate_to_datetime(published)
                    now = datetime.now(timezone.utc)
                    if now - pub_dt > timedelta(hours=36):
                        continue
            except Exception:
                pass
            
            summary_html = entry.get("summary", "")
            soup = BeautifulSoup(summary_html, "html.parser")
            summary_text = soup.get_text()[:300]
            
            news_items.append({
                "original_title": title,
                "original_url": link,
                "published_date": published,
                "summary_text": summary_text
            })
            
    print(f"Successfully retrieved data from {success_count} sources.")
    # Return at most 400 items so we don't blow out prompt limits excessively
    return news_items[:400]

if __name__ == "__main__":
    news = fetch_latest_news()
    print(f"Total collected items: {len(news)}")
