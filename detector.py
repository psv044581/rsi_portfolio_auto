"""Определяет новые и удалённые монеты относительно портфеля и config.py."""
import importlib
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, "/opt/claude-tg-bot")
sys.path.insert(0, "/home/klava/Rsi_Portfolio")
from portfolio_monitor import scrape_portfolio

logger = logging.getLogger(__name__)

KNOWN_FILE = Path("/home/klava/rsi_portfolio_auto/known_coins.json")
IGNORE = {"USD", "USDT", "USDC", "ETH", "BTC", "BNB"}


def _load_known() -> set:
    if KNOWN_FILE.exists():
        return set(json.loads(KNOWN_FILE.read_text()))
    return set()


def _save_known(coins: set) -> None:
    KNOWN_FILE.write_text(json.dumps(sorted(coins)))


def _get_portfolio_and_config() -> tuple[set[str], set[str]]:
    import config as cfg
    importlib.reload(cfg)
    existing = {c for coins in cfg.GROUPS.values() for c in coins}
    return cfg.PORTFOLIOS, existing


async def _scrape_portfolio_coins() -> set[str]:
    import config as cfg
    importlib.reload(cfg)
    coins: set[str] = set()
    for p in cfg.PORTFOLIOS:
        try:
            assets = await scrape_portfolio(p["url"])
            for a in assets:
                sym = a["symbol"].upper()
                if sym not in IGNORE:
                    coins.add(sym)
        except Exception as e:
            logger.error("Portfolio scrape error (%s): %s", p["name"], e)
    return coins


async def find_new_coins() -> list[str]:
    """Монеты из портфеля которых нет в GROUPS и не были уже обработаны."""
    known = _load_known()
    portfolio_coins = await _scrape_portfolio_coins()

    import config as cfg
    importlib.reload(cfg)
    existing = {c for coins in cfg.GROUPS.values() for c in coins}

    new_coins = portfolio_coins - existing - known
    if new_coins:
        logger.info("New coins detected: %s", new_coins)
    return sorted(new_coins)


async def find_removed_coins() -> list[str]:
    """Монеты которые есть в GROUPS но больше нет в портфеле."""
    portfolio_coins = await _scrape_portfolio_coins()

    import config as cfg
    importlib.reload(cfg)
    existing = {c for coins in cfg.GROUPS.values() for c in coins}

    removed = existing - portfolio_coins
    if removed:
        logger.info("Removed coins detected: %s", removed)
    return sorted(removed)


def mark_processed(symbol: str) -> None:
    known = _load_known()
    known.add(symbol)
    _save_known(known)
