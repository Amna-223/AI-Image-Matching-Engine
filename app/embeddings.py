import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

IMAGE_ANALYSIS_FILE = "data/image_analysis.json"
ARTICLES_FOLDER = "data/articles"
IMAGE_EMBEDDINGS_FILE = "data/image_embeddings.json"
ARTICLE_EMBEDDINGS_FILE = "data/article_embeddings.json"


def get_embedding(text: str) -> list[float]:
    """
    Send text to Gemini embedding model.
    Returns a vector — a list of numbers representing meaning.
    """
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values


def build_image_text(entry: dict) -> str:
    """
    Convert one image analysis entry into a single text string.
    We combine all fields because more context = better embedding.
    """
    analysis = entry["analysis"]

    product    = analysis.get("product", "")
    category   = analysis.get("category", "")
    attributes = ", ".join(analysis.get("attributes", []))
    description = analysis.get("description", "")

    return f"Product: {product}. Category: {category}. Attributes: {attributes}. Description: {description}"


def read_article(filepath: str) -> dict:
    """
    Read a .txt article file.
    First line = title.
    Rest = content.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Remove empty lines
    lines = [line for line in lines if line.strip()]

    title   = lines[0]
    content = " ".join(lines[1:])

    return {"title": title, "content": content}


def generate_image_embeddings():
    print("Generating Image Embeddings: \n")
    with open(IMAGE_ANALYSIS_FILE, "r", encoding="utf-8") as f:
        images = json.load(f)

    # Load already processed if file exists
    if os.path.exists(IMAGE_EMBEDDINGS_FILE):
        with open(IMAGE_EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
    else:
        results = []

    already_done = {entry["filename"] for entry in results}

    for entry in images:
        filename = entry["filename"]
        if filename in already_done:
            print(f"Skipping: {filename}")
            continue

        print(f"Embedding: {filename}")

        try:
            text   = build_image_text(entry)
            vector = get_embedding(text)

            results.append({
                "filename": filename,
                "category_folder": entry["category_folder"],
                "analysis": entry["analysis"],
                "text": text,
                "embedding": vector
            })

            # Save after every image
            with open(IMAGE_EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)

            print("Done")

        except Exception as e:
            print(f"Failed: {filename} — {e}")

    print(f"\nImage embeddings done. Total: {len(results)}")


def generate_article_embeddings():
    print("\nGenerating Article Embeddings\n")

    article_files = sorted([
        f for f in os.listdir(ARTICLES_FOLDER)
        if f.endswith(".txt")
    ])

    results = []

    for i, article_file in enumerate(article_files, start=1):
        filepath = os.path.join(ARTICLES_FOLDER, article_file)
        article  = read_article(filepath)

        print(f"Embedding: {article_file}")

        try:
            # Title + content together = richer embedding
            text   = f"{article['title']}. {article['content']}"
            vector = get_embedding(text)

            results.append({
                "article_id": i,
                "filename": article_file,
                "title": article["title"],
                "text": text,
                "embedding": vector
            })

            print(f"Done — {article['title']}")

        except Exception as e:
            print(f"Failed: {article_file} — {e}")

    with open(ARTICLE_EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\nArticle embeddings done. Total: {len(results)}")


if __name__ == "__main__":
    generate_image_embeddings()
    generate_article_embeddings()