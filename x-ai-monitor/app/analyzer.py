import logging
from datetime import datetime, timedelta

import anthropic

from . import database
from .config import get_config

logger = logging.getLogger(__name__)

MODEL = "claude-haiku-4-5-20251001"


def _compress(tweet: dict) -> str:
    text = tweet["text"][:50].replace("|", "｜").replace("\n", " ")
    date_mmdd = tweet["collected_date"][5:].replace("-", "")  # MMDD
    return f"tw:{text}|l:{tweet['likes']}|rt:{tweet['retweets']}|d:{date_mmdd}"


def analyze_weekly() -> str:
    """Fetch 7 days of stored tweets, compress, send to Claude, persist result.

    Returns the analysis text.
    Raises RuntimeError when configuration or data is missing.
    """
    cfg = get_config()
    if not cfg.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY が未設定です。/config から設定してください。")

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")

    tweets = database.get_tweets_by_date_range(start_date, end_date)
    if not tweets:
        raise RuntimeError(f"分析対象ツイートがありません（{start_date} 〜 {end_date}）。先にデータを収集してください。")

    compressed_body = "\n".join(_compress(t) for t in tweets)
    keyword = cfg.monitor_keyword

    system_prompt = f"""あなたはX（旧Twitter）のツイートアナリストです。
キーワード「{keyword}」に関する直近7日分のツイートを分析してください。

入力フォーマット: tw:本文|l:いいね数|rt:RT数|d:日付(MMDD)

以下を簡潔に日本語で報告してください:
1. 全体センチメント（ポジティブ / ネガティブ / 中立）
2. 主なトピックと傾向（3点箇条書き）
3. 注目ツイート（いいね・RT 上位 2〜3 件の要約）
4. 総合評価（3行以内）"""

    client = anthropic.Anthropic(api_key=cfg.anthropic_api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"【期間】{start_date} 〜 {end_date}\n"
                    f"【件数】{len(tweets)} 件\n\n"
                    f"{compressed_body}"
                ),
            }
        ],
    )

    result = response.content[0].text
    database.insert_analysis(start_date, end_date, keyword, result)
    logger.info("Analysis complete: %d tweets, keyword=%s", len(tweets), keyword)
    return result
