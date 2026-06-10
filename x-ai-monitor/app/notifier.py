import logging

import httpx

from .config import get_config

logger = logging.getLogger(__name__)


def send_telegram(message: str) -> bool:
    """Send a message via Telegram Bot API. Returns True on success."""
    cfg = get_config()
    if not cfg.telegram_bot_token or not cfg.telegram_chat_id:
        logger.warning("Telegram not configured; skipping notification.")
        return False

    url = f"https://api.telegram.org/bot{cfg.telegram_bot_token}/sendMessage"
    try:
        resp = httpx.post(
            url,
            json={"chat_id": cfg.telegram_chat_id, "text": message, "parse_mode": "HTML"},
            timeout=15,
        )
        resp.raise_for_status()
        logger.info("Telegram notification sent.")
        return True
    except httpx.HTTPError as e:
        logger.error("Telegram send failed: %s", e)
        return False
