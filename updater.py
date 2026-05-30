"""Обновляет config.py в Rsi_Portfolio при добавлении новой монеты."""
import asyncio
import logging
import re
import subprocess
import sys

logger = logging.getLogger(__name__)

CONFIG_PATH = "/home/klava/Rsi_Portfolio/config.py"
SERVICE_NAME = "rsi_portfolio"


def _read_config() -> str:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return f.read()


def _write_config(text: str) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(text)


def add_coin(symbol: str, group: int, comment: str, is_gate: bool) -> bool:
    text = _read_config()

    # Проверяем что монеты ещё нет
    if f'"{symbol}"' in text or f"'{symbol}'" in text:
        logger.info("%s already in config", symbol)
        return False

    # Добавляем в GROUPS[group]
    pattern = rf'({group}:\s*\[)([^\]]*?)(\])'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        logger.error("Group %d not found in config", group)
        return False

    old_list = match.group(0)
    # Добавляем монету в конец списка группы
    new_list = re.sub(
        r'(\s*\])',
        f', "{symbol}"\\1',
        old_list,
        count=1
    )
    text = text[:match.start()] + new_list + text[match.end():]

    # Добавляем в COIN_NOTES если есть комментарий
    if comment:
        notes_match = re.search(r'(COIN_NOTES\s*=\s*\{)', text)
        if notes_match:
            insert_pos = notes_match.end()
            text = text[:insert_pos] + f'\n    "{symbol}": "{comment}",' + text[insert_pos:]

    # Добавляем в GATE_COINS если нужно
    if is_gate:
        gate_match = re.search(r'(GATE_COINS\s*=\s*\{)([^}]*?)(\})', text, re.DOTALL)
        if gate_match:
            old_gate = gate_match.group(0)
            new_gate = re.sub(r'(\s*\})', f', "{symbol}"\\1', old_gate, count=1)
            text = text[:gate_match.start()] + new_gate + text[gate_match.end():]

    _write_config(text)
    logger.info("Added %s to config (group=%d, gate=%s)", symbol, group, is_gate)

    # Сразу регенерируем HTML и деплоим
    asyncio.run(_regenerate_and_deploy())

    return True


def remove_coin(symbol: str) -> bool:
    text = _read_config()

    if f'"{symbol}"' not in text and f"'{symbol}'" not in text:
        logger.info("%s not found in config", symbol)
        return False

    # Убираем из GROUPS (все вхождения в списках)
    text = re.sub(rf',?\s*"{symbol}"', "", text)
    text = re.sub(rf'"{symbol}",?\s*', "", text)

    # Убираем из COIN_NOTES
    text = re.sub(rf'\s*"{symbol}":\s*"[^"]*",?\n?', "\n", text)

    # Убираем из GATE_COINS
    text = re.sub(rf',?\s*"{symbol}"', "", text)

    _write_config(text)
    logger.info("Removed %s from config", symbol)

    asyncio.run(_regenerate_and_deploy())
    return True


async def _regenerate_and_deploy() -> None:
    sys.path.insert(0, "/home/klava/Rsi_Portfolio")
    import importlib
    # Перезагружаем config чтобы подхватить новые монеты
    import config
    importlib.reload(config)
    import data_fetcher
    importlib.reload(data_fetcher)

    try:
        from data_fetcher import fetch_all_data
        from html_generator import generate_html
        from github_deploy import deploy_to_github

        data = await fetch_all_data()
        if data:
            generate_html(data)
            await deploy_to_github()
            logger.info("HTML regenerated and deployed after coin addition")
    except Exception as e:
        logger.error("Regeneration failed: %s", e)
