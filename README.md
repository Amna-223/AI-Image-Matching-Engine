# AI Image Understanding & Content Matching Engine

A system that analyzes product images using AI vision, converts them into semantic embeddings, and matches them to the most relevant articles — based on meaning, not keywords.

## What it does

1. Takes a product image
2. Uses Gemini Vision to understand what's in it
3. Converts that understanding into a semantic embedding (vector)
4. Compares it against article embeddings
5. Returns the most relevant articles ranked by similarity

## Architecture
Product Image
↓
Gemini Vision
(structured analysis: product, category, attributes, description)
↓
Text Representation
↓
Gemini Embedding Model
↓
Image Vector
↓
FAISS Vector Search against Article Vectors
↓
Ranked Matching Articles + Similarity Scores


## Project Structure
AI-Image-Matching-Engine/
├── app/
│ ├── batch_process.py # Vision analysis batch job
│ ├── schemas.py # Pydantic validation schemas
│ └── main.py # FastAPI app (Phase 4)
├── data/
│ ├── images/ # 50 product images (5 categories x 10)
│ ├── articles/ # 10 .txt articles
│ └── image_analysis.json # Gemini vision output
├── .env.example
├── requirements.txt
└── README.md


## Tech Stack

- Python
- Google Gemini API (vision + embeddings)
- FAISS (vector similarity search)
- FastAPI
- Pydantic

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/flyrank-capstone-imagerelevance
cd flyrank-capstone-imagerelevance

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Open .env and add your GEMINI_API_KEY

# 5. Run vision batch processing
python -m app.batch_process
```

## Run the API

```bash
python -m app.main
```

## Dataset

- 50 product images across 5 categories: cameras, headphones, laptops, smartphones, wearables
- 10 articles covering each product category
- All images sourced from Pexels (free license)

## Evaluation

Top-1 precision measured on labeled eval set — results in EVIDENCE.md

## Limitations

- Fixed dataset of 50 images and 10 articles — small scale by design
- No user authentication
- No frontend — API only