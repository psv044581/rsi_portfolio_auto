"""
RSI Portfolio Auto — автоматически исследует новые монеты из портфеля
и добавляет их в Rsi_Portfolio/config.py
"""
import asyncio
import logging
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

LOG_FILE = "/home/klava/rsi_portfolio_auto/rsi_auto.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


async def check_and_research() -> None:
    from detector import find_new_coins, mark_processed
    from researcher import research_coin
    from updater import add_coin

    logger.info("=== Checking for new coins ===")
    new_coins = await find_new_coins()

    if not new_coins:
        logger.info("No new coins found")
        return

    for symbol in new_coins:
        logger.info("Researching %s...", symbol)
        result = research_coin(symbol)

        if result:
            added = add_coin(
                symbol=result["symbol"],
                group=result["group"],
                comment=result["comment"],
                is_gate=result["is_gate"],
            )
            if added:
                logger.info("✓ Added %s → group %d", symbol, result["group"])
        else:
            logger.warning("Research failed for %s, skipping", symbol)

        # Помечаем как обработанную в любом случае (чтобы не повторять)
        mark_processed(symbol)

    logger.info("=== Done ===")


async def main() -> None:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        check_and_research,
        IntervalTrigger(hours=1),
        id="check_coins",
        name="Hourly coin check",
    )

    scheduler.start()
    logger.info("RSI Auto started. Checking for new coins every hour.")

    # Запустить сразу при старте
    await check_and_research()

    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
