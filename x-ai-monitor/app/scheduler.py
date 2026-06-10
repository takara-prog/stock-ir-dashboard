import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from . import database
from .config import get_config

logger = logging.getLogger(__name__)

_WEEKDAY_MAP = {
    "MON": "mon", "TUE": "tue", "WED": "wed",
    "THU": "thu", "FRI": "fri", "SAT": "sat", "SUN": "sun",
}

scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")


async def run_collect() -> None:
    from . import collector
    try:
        count = await asyncio.to_thread(collector.collect_tweets)
        database.set_setting("last_collect_at", datetime.utcnow().isoformat())
        database.set_setting("last_collect_count", str(count))
        database.set_setting("last_collect_error", "")
        logger.info("Scheduled collect: %d tweets", count)
    except Exception as exc:
        logger.error("Scheduled collect failed: %s", exc)
        database.set_setting("last_collect_error", str(exc))


async def run_analyze() -> None:
    from . import analyzer, notifier
    try:
        result = await asyncio.to_thread(analyzer.analyze_weekly)
        database.set_setting("last_analyze_at", datetime.utcnow().isoformat())
        database.set_setting("last_analyze_error", "")
        cfg = get_config()
        await asyncio.to_thread(
            notifier.send_telegram,
            f"📊 <b>X AI Monitor 週次レポート</b>\nキーワード: {cfg.monitor_keyword}\n\n{result}",
        )
    except Exception as exc:
        logger.error("Scheduled analyze failed: %s", exc)
        database.set_setting("last_analyze_error", str(exc))


def setup_scheduler() -> None:
    """(Re-)register cron jobs based on current config."""
    cfg = get_config()
    collect_hour = cfg.collect_hour
    weekday = _WEEKDAY_MAP.get(cfg.analyze_weekday.upper(), "mon")

    scheduler.add_job(
        run_collect,
        CronTrigger(hour=collect_hour, minute=0, timezone="Asia/Tokyo"),
        id="collect",
        replace_existing=True,
    )
    scheduler.add_job(
        run_analyze,
        CronTrigger(day_of_week=weekday, hour=collect_hour + 1, minute=0, timezone="Asia/Tokyo"),
        id="analyze",
        replace_existing=True,
    )
    logger.info(
        "Scheduler configured: collect at %02d:00 daily, analyze on %s at %02d:00",
        collect_hour, weekday, collect_hour + 1,
    )


def start() -> None:
    setup_scheduler()
    scheduler.start()


def stop() -> None:
    scheduler.shutdown(wait=False)
