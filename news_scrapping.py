import feedparser

def get_agri_news():

    url = "https://news.google.com/rss/search?q=agriculture+india"

    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:5]:
        news_list.append(entry.title)

    return news_list

news = get_agri_news()

def prepare_news_summary(news):

    combined = "\n".join(news)

    return combined


print(prepare_news_summary(news))