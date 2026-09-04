import json
import os
from datetime import datetime

COST_LOG_FILE = "data/cost_log.json"

COST_PER_VISION_CALL = 0.0
COST_PER_EMBEDDING_CALL = 0.0


def log_call(call_type: str, model: str, details: str = ""):
    """
    Log every Gemini API call with timestamp.
    call_type: "vision" or "embedding"
    """

    if os.path.exists(COST_LOG_FILE):
        with open(COST_LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = []

    entry = {
        "timestamp": datetime.now().isoformat(),
        "call_type": call_type,
        "model": model,
        "details": details,
        "cost_usd": COST_PER_VISION_CALL if call_type == "vision" else COST_PER_EMBEDDING_CALL
    }

    log.append(entry)

    with open(COST_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=4)