

from typing import Any

# User storage: user_id -> user_dict
USERS: dict[str, dict[str, Any]] = {}

# Token storage: access_token -> user_id
TOKENS: dict[str, str] = {}

# Portfolio storage: portfolio_id -> portfolio_dict
PORTFOLIOS: dict[int, dict[str, Any]] = {}

# Market analysis results: analysis_id -> analysis_dict
ANALYSES: dict[int, dict[str, Any]] = {}

# Auto-incrementing IDs
NEXT_IDS = {
    "portfolio": 1,
    "holding": 1,
    "analysis": 1,
}


def get_next_id(key: str) -> int:
    """Get next ID and increment the counter."""
    val = NEXT_IDS[key]
    NEXT_IDS[key] += 1
    return val
