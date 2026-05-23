import sys
sys.stdout.reconfigure(encoding='utf-8')

from news_fetcher import fetch_news

import time
import pandas as pd

from news_fetcher import fetch_news
from sentiment import analyze_sentiment
from decision import get_signal
from telegram_bot import send_message

def run_bot():

    news_list = fetch_news()

    for news in news_list:

        label, score = analyze_sentiment(news)

        signal = get_signal(label, score)

        message = f"""
 News: {news}

Sentiment: {label} ({round(score,2)})

Signal: {signal}
"""

        print(message.encode("utf-8", errors="ignore").decode("utf-8"))

        send_message(message)

        # save log
        df = pd.DataFrame([[news, label, score, signal]],
                          columns=["news", "sentiment", "score", "signal"])

        df.to_csv("logs.csv", mode="a", header=False, index=False)


if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(300)  # 5 minutes