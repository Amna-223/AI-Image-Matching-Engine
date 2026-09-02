import json
import numpy as np
import faiss


ARTICLE_EMBEDDINGS_FILE = "data/article_embeddings.json"
IMAGE_EMBEDDINGS_FILE = "data/image_embeddings.json"


def load_article_index():
    """
    Load article embeddings into a FAISS index.
    Returns the index and the article metadata list.
    
    Why FAISS?
    Because it lets us search 'which article vector is closest
    to this image vector' instantly, even at larger scales.
    """

    with open(ARTICLE_EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Convert embeddings to numpy array — FAISS requires this format
    vectors = np.array(
        [article["embedding"] for article in articles],
        dtype=np.float32
    )

    # Normalize vectors for cosine similarity
    # Without this, FAISS measures raw distance, not cosine similarity
    faiss.normalize_L2(vectors)

    # Build flat index: simple exact search, perfect for 10 articles
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)  # IP = Inner Product = cosine after normalization
    index.add(vectors)

    print(f"FAISS index built with {index.ntotal} articles.")

    return index, articles


def search(query_embedding: list[float], index, articles: list, top_k: int = 3) -> list[dict]:
    """
    Given an image embedding, find the top_k most similar articles.
    Returns a ranked list with similarity scores.
    """

    # Convert to numpy and normalize
    query_vector = np.array([query_embedding], dtype=np.float32)
    faiss.normalize_L2(query_vector)

    # Search
    scores, indices = index.search(query_vector, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "article_id": articles[idx]["article_id"],
            "title": articles[idx]["title"],
            "filename": articles[idx]["filename"],
            "similarity": round(float(score), 4)
        })

    return results