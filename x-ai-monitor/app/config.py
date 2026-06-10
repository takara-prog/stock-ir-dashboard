import os
from dataclasses import dataclass


@dataclass
class Config:
    twitter_api_key: str
    anthropic_api_key: str
    telegram_bot_token: str
    telegram_chat_id: str
    monitor_keyword: str
    collect_hour: int
    analyze_weekday: str


def get_config() -> Config:
    """Load config: DB overrides take precedence over .env."""
    from . import database

    def resolve(db_key: str, env_key: str, default: str = "") -> str:
        db_val = database.get_setting(db_key)
        return db_val if db_val else os.getenv(env_key, default)

    return Config(
        twitter_api_key=resolve("twitter_api_key", "TWITTER_API_KEY"),
        anthropic_api_key=resolve("anthropic_api_key", "ANTHROPIC_API_KEY"),
        telegram_bot_token=resolve("telegram_bot_token", "TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=resolve("telegram_chat_id", "TELEGRAM_CHAT_ID"),
        monitor_keyword=resolve("monitor_keyword", "MONITOR_KEYWORD", "株"),
        collect_hour=int(resolve("collect_hour", "COLLECT_HOUR", "8")),
        analyze_weekday=resolve("analyze_weekday", "ANALYZE_WEEKDAY", "MON"),
    )
