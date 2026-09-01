import os
import json

from dotenv import load_dotenv
from google import genai
from PIL import Image

from app.schemas import ImageAnalysis


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


IMAGES_FOLDER = "data/images"
OUTPUT_FILE = "data/image_analysis.json"


prompt = """
Analyze this product image.

Return ONLY valid JSON in exactly this structure:

{
    "product": "name of the product",
    "category": "product category",
    "attributes": [
        "attribute 1",
        "attribute 2",
        "attribute 3"
    ],
    "description": "short description of the product"
}

Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.
"""


# Load existing results
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        results = json.load(file)
else:
    results = []


# Build a set of already-processed filenames (fix: track by name, not count)
processed_files = {entry["filename"] for entry in results}

print(f"Already processed: {len(processed_files)} images")
print()


for category in os.listdir(IMAGES_FOLDER):

    category_path = os.path.join(IMAGES_FOLDER, category)

    if not os.path.isdir(category_path):
        continue

    for filename in os.listdir(category_path):

        # Skip already processed images by filename
        if filename in processed_files:
            print(f"Skipping: {filename}")
            continue

        image_path = os.path.join(category_path, filename)

        print(f"Processing: {filename}")

        try:
            image = Image.open(image_path)

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    image,
                    prompt
                ]
            )

            data = json.loads(response.text)

            analysis = ImageAnalysis(**data)

            results.append({
                "filename": filename,
                "category_folder": category,
                "analysis": analysis.model_dump()
            })

            # Save after every successful image
            with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    results,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("✓ Success")

        except Exception as error:

            print(f"✗ Failed: {filename}")
            print(error)


print("\nFinished!")
print(f"Successfully processed: {len(results)} images")
print(f"Results saved to: {OUTPUT_FILE}")