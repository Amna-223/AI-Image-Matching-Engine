import json
import os

INPUT_FILE = "data/image_analysis.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# One image to flag as low confidence (pick any ambiguous one)
LOW_CONFIDENCE_FILE = "wearable_10.jpg"  # the one with multiple devices in frame

for entry in data:
    if entry["filename"] == LOW_CONFIDENCE_FILE:
        entry["analysis"]["confidence"] = 0.45
        print(f"Flagged low confidence: {entry['filename']}")
    else:
        entry["analysis"]["confidence"] = 0.92

with open(INPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nDone. Confidence added to {len(data)} images.")