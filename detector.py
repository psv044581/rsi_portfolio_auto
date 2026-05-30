"""Определяет новые монеты в портфеле которых нет в config.py."""
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, "/opt/claude-tg-bot")
sys.path.insert(0, "/home/klava/Rsi_Portfolio")
from portfolio_monitor import scrape_portfolio
from config import GROUPS, PORTFOLIOS

logger = logging.getLogger(__name__)

KNOWN_FILE = Path("/home/klava/rsi_portfolio_auto/known_coins.json")

COIN_TO_GROUP = {c for coins in GROUPS.values() for c in coins}

IGNORE = {"USD", "USDT", "USDC", "ETH", "BTC", "BNB"}


def _load_known() -> set:
    if KNOWN_FILE.exists():
        return set(json.loads(KNOWN_FILE.read_text()))
    return set()


def _save_known(coins: set) -> None:
    KNOWN_FILE.write_text(json.dumps(sorted(coins)))


async def find_new_coins() -> list[str]:
    """Возвращает монеты из портфеля которых нет в GROUPS и не были уже обработаны."""
    known = _load_known()

    portfolio_coins: set[str] = set()
    for p in PORTFOLIOS:
        try:
            assets = await scrape_portfolio(p["url"])
            for a in assets:
                sym = a["symbol"].upper()
                if sym not in IGNORE:
                    portfolio_coins.add(sym)
        except Exception as e:
            logger.error("Portfolio scrape error (%s): %s", p["name"], e)

    # Импортируем свежий config чтобы учесть уже добавленные монеты
    import importlib
    import config as cfg
    importlib.reload(cfg)
    existing = {c for coins in cfg.GROUPS.values() for c in coins}

    new_coins = portfolio_coins - existing - known
    if new_coins:
        logger.info("New coins detected: %s", new_coins)
    return sorted(new_coins)


def mark_processed(symbol: str) -> None:
    known = _load_known()
    known.add(symbol)
    _save_known(known)
