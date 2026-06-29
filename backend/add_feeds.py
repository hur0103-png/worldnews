import re
with open("crawler.py", "r", encoding="utf-8") as f:
    content = f.read()

new_feeds = """
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
"""

content = content.replace('    # Global/Orgs\n    "https://news.un.org/feed/subscribe/en/news/all/rss.xml",', new_feeds.strip("\n"))

with open("crawler.py", "w", encoding="utf-8") as f:
    f.write(content)
