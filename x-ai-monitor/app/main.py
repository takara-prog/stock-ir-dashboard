import asyncio
import logging
import random
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from . import database, scheduler as sched
from .config import get_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    sched.start()
    yield
    sched.stop()


app = FastAPI(title="X AI Monitor", lifespan=lifespan)


# ---- Helpers ----

def _mask(key: str) -> str:
    if not key:
        return ""
    return "****" + key[-4:] if len(key) > 4 else "****"


# ---- Routes ----

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    tweets = database.get_tweets_last_7_days()
    analysis = database.get_latest_analysis()
    cfg = get_config()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tweets": tweets,
        "analysis": analysis,
        "keyword": cfg.monitor_keyword,
        "tweet_count": len(tweets),
    })


@app.get("/config", response_class=HTMLResponse)
async def config_page(request: Request, saved: bool = False, error: str = ""):
    cfg = get_config()
    return templates.TemplateResponse("config.html", {
        "request": request,
        "cfg": cfg,
        "twitter_api_key_masked": _mask(cfg.twitter_api_key),
        "anthropic_api_key_masked": _mask(cfg.anthropic_api_key),
        "telegram_bot_token_masked": _mask(cfg.telegram_bot_token),
        "saved": saved,
        "error": error,
        "weekdays": ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
    })


@app.post("/config")
async def config_save(
    monitor_keyword: str = Form(...),
    collect_hour: int = Form(...),
    analyze_weekday: str = Form(...),
    twitter_api_key: str = Form(""),
    anthropic_api_key: str = Form(""),
    telegram_bot_token: str = Form(""),
    telegram_chat_id: str = Form(""),
):
    database.set_setting("monitor_keyword", monitor_keyword.strip())
    database.set_setting("collect_hour", str(max(0, min(23, collect_hour))))
    database.set_setting("analyze_weekday", analyze_weekday.upper())

    # Only update API keys if user provided a new value (not the masked placeholder)
    if twitter_api_key and not twitter_api_key.startswith("****"):
        database.set_setting("twitter_api_key", twitter_api_key.strip())
    if anthropic_api_key and not anthropic_api_key.startswith("****"):
        database.set_setting("anthropic_api_key", anthropic_api_key.strip())
    if telegram_bot_token and not telegram_bot_token.startswith("****"):
        database.set_setting("telegram_bot_token", telegram_bot_token.strip())
    if telegram_chat_id.strip():
        database.set_setting("telegram_chat_id", telegram_chat_id.strip())

    # Reload scheduler with new timing
    sched.setup_scheduler()

    return RedirectResponse("/config?saved=1", status_code=303)


@app.get("/status", response_class=HTMLResponse)
async def status(request: Request):
    cfg = get_config()
    collect_job = sched.scheduler.get_job("collect")
    analyze_job = sched.scheduler.get_job("analyze")
    next_collect = str(collect_job.next_run_time) if collect_job else "N/A"
    next_analyze = str(analyze_job.next_run_time) if analyze_job else "N/A"

    return templates.TemplateResponse("status.html", {
        "request": request,
        "cfg": cfg,
        "collect_status": database.get_collect_status(),
        "analyses": database.get_analyses_history(limit=5),
        "last_collect_at": database.get_setting("last_collect_at"),
        "last_analyze_at": database.get_setting("last_analyze_at"),
        "last_collect_count": database.get_setting("last_collect_count"),
        "last_collect_error": database.get_setting("last_collect_error"),
        "last_analyze_error": database.get_setting("last_analyze_error"),
        "next_collect": next_collect,
        "next_analyze": next_analyze,
    })


# ---- Admin actions ----

@app.post("/admin/collect")
async def manual_collect():
    await sched.run_collect()
    return RedirectResponse("/status", status_code=303)


@app.post("/admin/analyze")
async def manual_analyze():
    await sched.run_analyze()
    return RedirectResponse("/?analyzed=1", status_code=303)


@app.post("/admin/mock")
async def generate_mock():
    """Insert 7 days × 10 tweets of mock data for testing."""
    MOCK_TEMPLATES = [
        "{kw}関連銘柄が急騰！市場は一転して強気ムードに。今日の取引を振り返ると……",
        "{kw}の動向に注目。専門家は「今後3ヶ月が重要な転換点」と分析している。",
        "{kw}に資金流入が続く。個人投資家のセンチメントが改善している模様。",
        "【速報】{kw}市場でサプライズ！想定外の発表に投資家が反応。",
        "{kw}をめぐる海外投資家の動向が気になる。円安・円高どちらに振れる？",
        "今週の{kw}まとめ。上昇トレンドが継続するか、調整局面を迎えるか。",
        "{kw}関連の決算発表が相次ぐ。業績見通しは総じて堅調。",
        "米国市場の動向が{kw}にも影響。東京市場は様子見姿勢か。",
        "{kw}の長期保有を検討中。配当利回りと成長性のバランスが魅力。",
        "初心者でもわかる{kw}入門。まずは少額から始めてみよう！",
    ]

    cfg = get_config()
    kw = cfg.monitor_keyword
    inserted = 0

    for days_ago in range(7):
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        for i, tmpl in enumerate(MOCK_TEMPLATES):
            tweet_id = f"mock_{date}_{i}"
            text = tmpl.format(kw=kw)
            ok = database.insert_tweet(
                tweet_id=tweet_id,
                text=text,
                likes=random.randint(0, 300),
                retweets=random.randint(0, 80),
                collected_date=date,
                author_id=f"mockuser_{i}",
                created_at=f"{date}T09:00:00Z",
                raw_json="{}",
            )
            if ok:
                inserted += 1

    return RedirectResponse(f"/?mock={inserted}", status_code=303)
