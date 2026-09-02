from app.vector_store import load_article_index, search

SIMILARITY_THRESHOLD = 0.60
CONFIDENCE_THRESHOLD = 0.60

ARTICLE_CATEGORY_MAP = {
    "article_01.txt": ["smartphone", "mobile", "phone", "electronics"],
    "article_02.txt": ["laptop", "computer", "notebook"],
    "article_03.txt": ["headphone", "audio", "sound", "earphone", "wireless", "earbud"],
    "article_04.txt": ["wearable", "smartwatch", "watch", "fitness", "tracker"],
    "article_05.txt": ["camera", "photography", "photo", "lens", "film"],
    "article_06.txt": ["smartphone", "laptop", "headphone", "wearable", "smartwatch", "camera", "wireless", "electronics"],
    "article_07.txt": ["laptop", "smartphone", "headphone", "wearable", "smartwatch", "productivity", "electronics"],
    "article_08.txt": ["smartphone", "laptop", "headphone", "smartwatch", "camera", "bluetooth", "wifi", "wireless", "electronics"],
    "article_09.txt": ["camera", "smartphone", "laptop", "headphone", "photography", "content", "electronics"],
    "article_10.txt": ["smartphone", "laptop", "headphone", "smartwatch", "wearable", "camera", "electronics"],
}

GENERIC_ARTICLES = {
    "article_06.txt",
    "article_07.txt",
    "article_08.txt",
    "article_09.txt",
    "article_10.txt",
}

GENERIC_PENALTY = 0.03


def apply_penalty(candidates: list) -> list:
    adjusted = []
    for candidate in candidates:
        score = candidate["similarity"]
        if candidate["filename"] in GENERIC_ARTICLES:
            score = score - GENERIC_PENALTY
        adjusted.append({**candidate, "similarity": round(score, 4)})
    adjusted.sort(key=lambda x: x["similarity"], reverse=True)
    return adjusted


def check_category_match(image_category: str, article_filename: str) -> bool:
    image_cat_lower = image_category.lower()
    keywords = ARTICLE_CATEGORY_MAP.get(article_filename, [])
    return any(keyword in image_cat_lower for keyword in keywords)


def match_image_to_articles(image_entry: dict, index, articles: list) -> dict:

    filename = image_entry["filename"]
    analysis = image_entry["analysis"]
    embedding = image_entry["embedding"]
    confidence = analysis.get("confidence", 0.92)
    image_category = analysis.get("category", "")

    # Step 1 — confidence check
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "filename": filename,
            "status": "REJECTED",
            "reason": f"Low confidence score ({confidence}) — image classification unreliable",
            "matches": []
        }

    # Step 2 — FAISS search
    candidates = search(embedding, index, articles, top_k=5)

    # Step 3 — apply penalty to generic articles
    candidates = apply_penalty(candidates)

    # Step 4 — find best candidate that passes both checks
    best_match = None
    for candidate in candidates:
        if candidate["similarity"] < SIMILARITY_THRESHOLD:
            continue
        if check_category_match(image_category, candidate["filename"]):
            best_match = candidate
            break

    # Step 5 — no candidate passed
    if best_match is None:
        top = candidates[0]
        return {
            "filename": filename,
            "status": "NO_MATCH",
            "reason": f"No article passed both similarity and category checks. Best similarity: {top['similarity']}",
            "matches": candidates
        }

    # Step 6 — accepted
    return {
        "filename": filename,
        "status": "MATCHED",
        "reason": "Similarity and category both cleared thresholds",
        "top_match": best_match,
        "all_candidates": candidates
    }