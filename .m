3commas_hft_bot/
│
├── .env                         # API keys and secrets (never commit)
├── .gitignore                   # Ignore virtual env, pyc, .env, etc.
├── Makefile                     # Automation commands
├── pyproject.toml               # Linting, typing, and tool config
├── requirements.txt             # For deployment/fallback environments
├── README.md                    # Project overview and setup instructions
│
├── bot/                         # Source code
│   ├── __init__.py
│   ├── main.py                  # Entry point to the bot
│   │
│   ├── config/                  # Configuration loading and validation
│   │   └── settings.py
│   │
│   ├── core/                    # Core engine
│   │   ├── bot_manager.py       # Bot initialization and control logic
│   │   ├── executor.py          # Executes orders via 3Commas API
│   │   ├── scheduler.py         # Handles intervals, jobs, retries
│   │   └── state.py             # Tracks runtime bot state, position info
│   │
│   ├── strategies/              # Different trading strategies
│   │   ├── __init__.py
│   │   ├── scalping.py
│   │   ├── arbitrage.py
│   │   └── grid.py
│   │
│   ├── exchange/                # Exchange & API interaction
│   │   ├── __init__.py
│   │   ├── threecommas_api.py   # Wrapper for 3Commas endpoints
│   │   └── market_data.py       # Market data fetching/parsing
│   │
│   ├── utils/                   # Helper functions
│   │   ├── __init__.py
│   │   ├── logger.py            # Logging setup
│   │   ├── notifier.py          # Webhooks, email, etc.
│   │   └── tools.py             # Miscellaneous utilities
│   │
│   └── models/                  # Typed data classes
│       ├── __init__.py
│       ├── trade.py
│       └── config.py
│
└── tests/                       # Unit & integration tests
    ├── __init__.py
    ├── test_main.py
    ├── strategies/
    │   └── test_scalping.py
    ├── core/
    │   └── test_executor.py
    └── exchange/
        └── test_threecommas_api.py
