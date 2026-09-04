import json
import os
from datetime import datetime

COST_LOG_FILE = "data/cost_log.json"
IMAGE_ANALYSIS_FILE = "data/image_analysis.json"
IMAGE_EMBEDDINGS_FILE = "data/image_embeddings.json"
ARTICLE_EMBEDDINGS_FILE = "data/article_embeddings.json"

log = []

# Vision calls — one per image in image_analysis.json
with open(IMAGE_ANALYSIS_FILE, "r", encoding="utf-8") as f:
    images = json.load(f)

for entry in images:
    log.append({
        "timestamp": datetime.now().isoformat(),
        "call_type": "vision",
        "model": "gemini-2.5-flash",
        "details": entry["filename"],
        "cost_usd": 0.0
    })

# Image embedding calls
with open(IMAGE_EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    image_embeddings = json.load(f)

for entry in image_embeddings:
    log.append({
        "timestamp": datetime.now().isoformat(),
        "call_type": "embedding",
        "model": "gemini-embedding-001",
        "details": entry["filename"],
        "cost_usd": 0.0
    })

# Article embedding calls
with open(ARTICLE_EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    article_embeddings = json.load(f)

for entry in article_embeddings:
    log.append({
        "timestamp": datetime.now().isoformat(),
        "call_type": "embedding",
        "model": "gemini-embedding-001",
        "details": entry["filename"],
        "cost_usd": 0.0
    })

with open(COST_LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(log, f, indent=4)

print(f"Cost log created: {len(log)} entries")
print(f"  Vision calls:    {len(images)}")
print(f"  Image embeddings: {len(image_embeddings)}")
print(f"  Article embeddings: {len(article_embeddings)}")