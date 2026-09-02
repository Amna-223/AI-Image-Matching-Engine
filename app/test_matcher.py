import json
from app.vector_store import load_article_index
from app.matcher import match_image_to_articles

# Load FAISS index
index, articles = load_article_index()

# Load both files
with open("data/image_embeddings.json", "r", encoding="utf-8") as f:
    embeddings = json.load(f)

with open("data/image_analysis.json", "r", encoding="utf-8") as f:
    analysis_data = json.load(f)

# Merge by filename
analysis_map = {entry["filename"]: entry["analysis"] for entry in analysis_data}

images = []
for emb_entry in embeddings:
    filename = emb_entry["filename"]
    images.append({
        "filename": filename,
        "category_folder": emb_entry["category_folder"],
        "analysis": analysis_map.get(filename, {}),
        "embedding": emb_entry["embedding"]
    })

# Track results
matched = []
rejected = []
no_match = []

for image_entry in images:
    result = match_image_to_articles(image_entry, index, articles)

    print(f"\n{'='*20}")
    print(f"Image:    {image_entry['filename']}")
    print(f"Category: {image_entry['analysis'].get('category', 'N/A')}")
    print(f"Status:   {result['status']}")
    print(f"Reason:   {result['reason']}")

    if result["status"] == "MATCHED":
        print(f"Match:    {result['top_match']['title']}")
        print(f"Score:    {result['top_match']['similarity']}")
        matched.append(image_entry["filename"])
    elif result["status"] == "REJECTED":
        rejected.append(image_entry["filename"])
    else:
        no_match.append(image_entry["filename"])

# Summary
print(f"\n{'='*40}")
print(f"SUMMARY")
print(f"{'='*40}")
print(f"Total images:  50")
print(f"Matched:       {len(matched)}")
print(f"Rejected:      {len(rejected)}")
print(f"No match:      {len(no_match)}")

if no_match:
    print(f"\nNo match images:")
    for f in no_match:
        print(f"  - {f}")

if rejected:
    print(f"\nRejected images:")
    for f in rejected:
        print(f"  - {f}")