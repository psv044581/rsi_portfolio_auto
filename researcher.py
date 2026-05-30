"""Исследует новую монету через claude CLI и возвращает группу риска + комментарий."""
import json
import logging
import os
import re
import subprocess
import tempfile

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты аналитик криптовалютного портфеля. Твоя задача — исследовать монету и присвоить группу риска.

Критерии групп:
1 — Критический риск: проект мёртв или делистится, просадка 87-99%
2 — Очень высокий риск: держать без усреднения
3 — Высокий риск: реальный проект с высоким риском
4 — Умеренно-высокий риск: избранные для докупки
5 — Умеренный риск: сильные фундаменталы, ближайшие к безубытку

Отвечай ТОЛЬКО валидным JSON, без markdown, без пояснений:
{"group": <1-5>, "comment": "<кратко о ключевых рисках, до 80 символов>", "is_gate": <true если монета только на Gate.io, false если есть на Binance>}"""


def research_coin(symbol: str) -> dict | None:
    prompt = (
        f"Исследуй крипто монету {symbol}. "
        f"Найди: проект, риски, разлоки, листинги (Binance/Gate.io). "
        f"Присвой группу риска 1-5 и напиши комментарий."
    )

    env = os.environ.copy()
    env["PATH"] = "/home/klava/.local/bin:" + env.get("PATH", "")

    try:
        result = subprocess.run(
            [
                "claude", "-p",
                "--model", "haiku",
                "--allowedTools", "WebSearch,WebFetch",
                "--output-format", "json",
                "--system-prompt", SYSTEM_PROMPT,
                "--no-session-persistence",
                prompt,
            ],
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )

        raw = result.stdout.strip() or result.stderr.strip()
        if not raw:
            logger.error("Empty response for %s", symbol)
            return None

        outer = json.loads(raw)
        text = outer.get("result", "")

        # Извлекаем JSON из ответа (может быть в markdown-блоке)
        json_match = re.search(r'\{[^{}]+\}', text, re.DOTALL)
        if not json_match:
            logger.error("No JSON found in response for %s: %s", symbol, text[:200])
            return None

        data = json.loads(json_match.group())
        group = int(data.get("group", 3))
        comment = str(data.get("comment", "")).strip()[:80]
        is_gate = bool(data.get("is_gate", False))

        if not 1 <= group <= 5:
            logger.error("Invalid group %d for %s", group, symbol)
            return None

        logger.info("Researched %s → group=%d gate=%s comment=%s", symbol, group, is_gate, comment)
        return {"symbol": symbol, "group": group, "comment": comment, "is_gate": is_gate}

    except subprocess.TimeoutExpired:
        logger.error("Timeout researching %s", symbol)
        return None
    except Exception as e:
        logger.error("Research error for %s: %s", symbol, e)
        return None
