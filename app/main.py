import json
import os
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from PIL import Image

from app.schemas import ImageAnalysis
from app.vector_store import load_article_index
from app.matcher import match_image_to_articles
from app.cost_tracker import log_call

load_dotenv()

app = FastAPI(
    title="AI Image Matching Engine",
    description="Matches product images to relevant articles using Gemini Vision and FAISS",
    version="1.0.0"
)

# Load FAISS index once at startup
index, articles = load_article_index()

with open("data/article_embeddings.json", "r", encoding="utf-8") as f:
    article_embeddings = json.load(f)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
    "description": "short description of the product",
    "confidence": 0.95
}

confidence must be a float between 0.0 and 1.0.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.
"""


@app.get("/")
def root():
    return {"message": "AI Image Matching Engine is running"}


@app.post("/match")
async def match_image(file: UploadFile = File(...)):
    """
    Upload a product image.
    Returns the most relevant articles based on semantic matching.
    """

    # Step 1 — validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Step 2 — save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # Step 3 — Gemini vision analysis
        image = Image.open(tmp_path)

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[image, prompt]
            )
        except genai_errors.ServerError:
            raise HTTPException(
                status_code=503,
                detail="Gemini model temporarily unavailable. Please try again later."
            )

        # Step 4 — validate response against schema
        try:
            data = json.loads(response.text)
            analysis = ImageAnalysis(**data)
            log_call("vision", "gemini-3.6-flash", file.filename)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid model response: {str(e)}"
            )

        # Step 5 — generate embedding
        embed_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        analysis_dict = analysis.model_dump()
        text = f"Product: {analysis_dict['product']}. Category: {analysis_dict['category']}. Attributes: {', '.join(analysis_dict['attributes'])}. Description: {analysis_dict['description']}"

        try:
            embed_response = embed_client.models.embed_content(
                model="models/gemini-embedding-001",
                contents=text
            )
            embedding = embed_response.embeddings[0].values
            log_call("embedding", "gemini-embedding-001", file.filename)
        except genai_errors.ServerError:
            raise HTTPException(
                status_code=503,
                detail="Gemini embedding model temporarily unavailable. Please try again later."
            )

        # Step 6 — match via FAISS + mismatch guard
        image_entry = {
            "filename": file.filename,
            "category_folder": "",
            "analysis": analysis_dict,
            "embedding": embedding
        }

        result = match_image_to_articles(image_entry, index, articles)

        # Step 7 — return response
        return JSONResponse(content={
            "image_analysis": analysis_dict,
            "matching_result": result
        })

    finally:
        os.unlink(tmp_path)


@app.get("/cost-log")
def get_cost_log():
    """
    View all API calls and their costs.
    """
    with open("data/cost_log.json", "r", encoding="utf-8") as f:
        log = json.load(f)

    total_calls = len(log)
    vision_calls = len([x for x in log if x["call_type"] == "vision"])
    embedding_calls = len([x for x in log if x["call_type"] == "embedding"])

    return {
        "total_calls": total_calls,
        "vision_calls": vision_calls,
        "embedding_calls": embedding_calls,
        "total_cost_usd": 0.0,
        "log": log
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)