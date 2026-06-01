import pytz

TIMEZONE = pytz.timezone("Europe/Podgorica")  # UTC+2

GROUPS = {
    1: ["OBT"],
    2: ["HFT", "FLOW"],
    3: ["IMX", "GRT", "JUP", "FIL", "W", "ARB", "CFX", "COMP", "ICP", "LDO", "NEAR", "RENDER", "TON", "DOT", "HBAR", "STRK", "OP", "ONDO", "XCH", "TIA", "WLD", "APT"],
    4: [, "ZK", "XRP", "BTC", "ROSE", "PYTH"],
    5: ["ETH"],
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
    "BTC": "Коррекция -43% от ATH, ETF оттоки, нет краткосрочных катализаторов",
    "FLOW":    "Хак Dec'25 + делистинг KR бирж, TVL $13M, governance-only токен",
    "OBT":     "Мёртвый проект: $22K объём, -99.95% ATH, нет revenue, инфляция",
    "HFT":     "мониторинг-тег Binance 22 мая 2026",
    "APT":     "P/S 82x при $9.3M ARR, конкур SOL/SUI, -95% ATH, кат. Oct26",
    "XCH":     "нет value capture, непрозрачный prefarm, -99.9% ATH, Permuto через 18мес",
    "ZK":      "Вестинг-давление до 2028, инфляция 20%+ циркуляции, но живой L2",
    "ARB":     "Живой L2, но массовые разблокировки (92M/мес), отток к конкурентам",
    "PYTH":    "Реальный adoption, buyback, но -97% ATH и 27% MCap разлок май 2027",
    "IMX":     "ZK-риски, игровой рынок волатилен, L2-конкуренция",
    "ROSE":    "Сильная команда/инвесторы, но нет revenue capture и слабый adoption",
    "GRT":     "Infinite supply, 3% инфляция, новый ATL фев 2026, реальный проект",
    "WLD":     "Инфляция 67%/год, уход топ-менеджеров, нет выручки",
    "TIA":     "Разлоки позади, но -98% ATH, инсайдер-продажи, мизерный доход",
    "JUP":     "Просадка ~79% от макс, зависимость от Solana, цена не растёт",
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
