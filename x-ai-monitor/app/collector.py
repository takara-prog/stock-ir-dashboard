import json
import logging
from datetime import datetime

import tweepy

from . import database
from .config import get_config

logger = logging.getLogger(__name__)


def collect_tweets() -> int:
    """Fetch up to 10 tweets matching the keyword and store them in SQLite.

    Returns the number of new tweets inserted.
    Raises RuntimeError on API or configuration errors.
    """
    cfg = get_config()
    if not cfg.twitter_api_key:
        raise RuntimeError("TWITTER_API_KEY が未設定です。/config から設定してください。")

    client = tweepy.Client(bearer_token=cfg.twitter_api_key, wait_on_rate_limit=False)
    today = datetime.now().strftime("%Y-%m-%d")
    query = f"{cfg.monitor_keyword} -is:retweet"

    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=10,
            tweet_fields=["public_metrics", "created_at", "author_id"],
        )
    except tweepy.errors.TweepyException as e:
        raise RuntimeError(f"Twitter API エラー: {e}") from e

    if not response.data:
        logger.info("No tweets found for query: %s", query)
        return 0

    count = 0
    for tweet in response.data:
        metrics = tweet.public_metrics or {}
        inserted = database.insert_tweet(
            tweet_id=str(tweet.id),
            text=tweet.text,
            likes=metrics.get("like_count", 0),
            retweets=metrics.get("retweet_count", 0),
            collected_date=today,
            author_id=str(tweet.author_id) if tweet.author_id else "",
            created_at=str(tweet.created_at) if tweet.created_at else "",
            raw_json=json.dumps(
                {"id": str(tweet.id), "text": tweet.text, "metrics": metrics},
                ensure_ascii=False,
            ),
        )
        if inserted:
            count += 1

    logger.info("Collected %d new tweets (keyword=%s)", count, cfg.monitor_keyword)
    return count
