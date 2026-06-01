import pytz

TIMEZONE = pytz.timezone("Europe/Podgorica")  # UTC+2

GROUPS = {
    1: [],
    2: ["HFT", "WLD", "APE"],
    3: ["IMX", "ROSE", "GRT", "JUP", "FIL", "W", "ARB", "CFX", "COMP", "FLOW", "ICP", "LDO", "NEAR", "OBT", "PYTH", "RENDER", "TON", "DOT", "HBAR", "STRK", "OP", "ONDO", "XCH", "TIA"],
    4: ["APT", "ZK", "XRP"],
    5: ["ETH", "BTC"],
}

GROUP_LABELS = {
    1: "🔴 Группа 1 — Критический риск: ПРОДАТЬ",
    2: "🟠 Группа 2 — Очень высокий риск: минимизировать",
    3: "🟡 Группа 3 — Высокий риск: держать/ждать",
    4: "🟡 Группа 4 — Умеренно-высокий риск: докупать избранные",
    5: "🟢 Группа 5 — Умеренный риск: приоритет",
}

GROUP_DESCRIPTIONS = {
    1: "просадка 87–99% / проекты мертвы или делистятся",
    2: "держать без усреднения",
    3: "высокий риск — реальные проекты",
    4: "избранные на докупку",
    5: "ближайшие к безубытку / сильные фундаменталы",
}

COIN_NOTES = {
    "XRP": "Регуляторная ясность + ETF, но нет revenue capture, ежемесячные escrow-разлоки",
    "OP": "Base ушёл (97% rev), разлок 30.06, buyback тезис под угрозой",
    "STRK": "revenue -99% от пика, governance-only, TVL 18x ниже конкурентов",
    "HBAR": "RWA-лидер, ETF, commodity-статус, но P/S>12000x и доход $330K/год",
    "DOT": "Нулевой revenue, спад активности, но hard cap+ETF+историческое дно",
    "BTC": "Топ-актив: ETF-спрос, SBR-нарратив, халвинг 2028, коррекция -43%",
    "FLOW":    "Разлоки завершены, buyback есть, но нет value capture и NFT нарратив мёртв",
    "OBT":     "Реал.выручка $50M но capture неясен; CertiK 3.9/10; -97.8% от ATH",
    "HFT":     "мониторинг-тег Binance 22 мая 2026",
    "APT":     "Анлоки до окт 2026 — давление на цену, конкуренция L1, волатильность",
    "XCH":     "нет value capture, непрозрачный prefarm, -99.9% ATH, Permuto через 18мес",
    "ZK":      "Вестинг-давление до 2028, инфляция 20%+ циркуляции, но живой L2",
    "ARB":     "Живой L2, но массовые разблокировки (92M/мес), отток к конкурентам",
    "PYTH":    "Слабая токеномика, 57.5% разблокировано, разлоки давят цену",
    "IMX":     "ZK-риски, игровой рынок волатилен, L2-конкуренция",
    "ROSE":    "Делистинг Корея, TEE-уязвимости, конкуренция, разлоки",
    "GRT":     "Infinite supply, 3% инфляция, новый ATL фев 2026, реальный проект",
    "WLD":     "24 июля 2026: разлок -43% (5.1M→2.9M WLD/день)",
    "TIA":     "Разлоки позади, но -98% ATH, инсайдер-продажи, мизерный доход",
    "JUP":     "Просадка ~79% от макс, зависимость от Solana, цена не растёт",
    "APE":     "NFT нарратив угас, нет revenue/buyback, -99.5% ATH, governance-only",
    "FIL":     "Долгий вестинг до 2050, высокий FDV $3B, риск дилюции, конкуренция",
    "ICP":     "Конкуренция Ethereum/Solana, низкая адопция dApps",
    "ONDO":    "Governance-only, разлок $690M (40% MCap), смерть CEO",
    "COMP":    "Реальный проект, но хак Kelp DAO апр 2026, давление инсайдеров",
    "TON":     "900M Telegram-пользователей",
    "CFX":     "Делистинги (Bitvavo), низкая ликвидность, критические баги",
    "RENDER":  "AI-GPU / +60K GPU в сети",
    "LDO":     "рассмотреть докупку при просадке",
    "NEAR":    "рассмотреть докупку при просадке",
    "W":       "Wormhole — кросс-чейн мост, конкуренция LayerZero/Axelar",
    "ETH":     "Ethereum — флагманский L1, ETF запущен, институциональный актив",
}

GATE_COINS = {"OBT", "XCH"}

PORTFOLIOS = [
    {"name": "по моим мыслям", "url": "https://dropstab.com/p/po-moim-myslam-fjkjsebo6f"},
]

# Путь к файлам gspread OAuth
GSPREAD_CREDENTIALS = "/home/klava/.config/gspread/credentials.json"
GSPREAD_TOKEN       = "/home/klava/.config/gspread/authorized_user.json"

# Куда сохранять HTML для хостинга
HTML_OUTPUT = "/home/klava/rsi_portfolio_auto/public/index.html"

# Логи
LOG_FILE = "/home/klava/rsi_portfolio_auto/rsi_portfolio.log"

# Пересчёт RSI — интервалы
RSI_INTERVAL      = "1d"
RSI_INTERVAL_WEEK = "1w"
RSI_PERIOD        = 14
OHLC_LIMIT        = 50
TOP_PAIRS         = 5  # у каждой монеты, внизу страницы — все

# GitHub Pages деплой
from _secrets import GH_TOKEN as GITHUB_TOKEN, GH_REPO as GITHUB_REPO
GITHUB_FILE  = "index.html"
