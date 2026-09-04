import json
from app.vector_store import load_article_index
from app.matcher import match_image_to_articles

EVAL_FILE = "data/eval_dataset.json"
IMAGE_EMBEDDINGS_FILE = "data/image_embeddings.json"
IMAGE_ANALYSIS_FILE = "data/image_analysis.json"

# Load everything
index, articles = load_article_index()

with open(EVAL_FILE, "r", encoding="utf-8") as f:
    eval_data = json.load(f)

with open(IMAGE_EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    embeddings = json.load(f)

with open(IMAGE_ANALYSIS_FILE, "r", encoding="utf-8") as f:
    analysis_data = json.load(f)

# Merge by filename
analysis_map = {e["filename"]: e["analysis"] for e in analysis_data}
embedding_map = {e["filename"]: e["embedding"] for e in embeddings}

# Run eval
correct = 0
wrong = 0
rejected = 0
total = 0

print(f"{'Image':<25} {'Expected':<20} {'Got':<20} {'Result'}")
print("-" * 80)

for item in eval_data:
    filename = item["filename"]
    expected = item["expected_article"]

    if filename not in embedding_map:
        continue

    image_entry = {
        "filename": filename,
        "category_folder": filename.split("_")[0] + "s",
        "analysis": analysis_map.get(filename, {}),
        "embedding": embedding_map[filename]
    }

    result = match_image_to_articles(image_entry, index, articles)

    total += 1

    if result["status"] == "MATCHED":
        got = result["top_match"]["filename"]
        if got == expected:
            correct += 1
            status = "CORRECT"
        else:
            wrong += 1
            status = "WRONG"
    elif result["status"] == "REJECTED":
        got = "REJECTED"
        rejected += 1
        status = "REJECTED (low confidence)"
    else:
        got = "NO_MATCH"
        wrong += 1
        status = "WRONG"

    print(f"{filename:<25} {expected:<20} {got:<20} {status}")

print("-" * 80)
print(f"\nTotal:     {total}")
print(f"Correct:   {correct}")
print(f"Wrong:     {wrong}")
print(f"Rejected:  {rejected} (intentional low confidence)")
print(f"\nTop-1 Precision (matched only): {correct/(total-rejected):.2%}")
print(f"Top-1 Precision (all):          {correct/total:.2%}")