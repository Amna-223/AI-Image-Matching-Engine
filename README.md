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
## Project Structure

```
AI-Image-Matching-Engine/
├── app/
│   ├── batch_process.py         
│   ├── embeddings.py            
│   ├── add_confidence.py        
│   ├── vector_store.py          
│   ├── matcher.py               
│   ├── test_matcher.py          
│   ├── schemas.py               
│   └── main.py                  
├── data/
│   ├── images/                
│   ├── articles/              
│   ├── image_analysis.json    
│   ├── image_embeddings.json    
│   └── article_embeddings.json
├── .env.example
├── requirements.txt
├── .gitignore
├── capstone.yaml
├── BUILDLOG.md
├── EVIDENCE.md
└── README.md
```

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

## Evaluation Results

Evaluated on 50 labeled images across 5 categories.

| Metric | Value |
|--------|-------|
| Total images | 50 |
| Correct matches | 47 |
| Wrong matches | 2 |
| Intentional rejections | 1 |
| Top-1 Precision (matched only) | 95.92% |
| Top-1 Precision (all) | 94.00% |

### Notes
- laptop_06 and laptop_07 matched a generic multi-category article
  instead of the laptop article — Gemini assigned "Electronics" as
  category instead of "Laptops", causing category check to fail.
- wearable_10 correctly rejected due to low confidence (0.45) —
  image contains multiple devices in one frame.

## Limitations

- Fixed dataset of 50 images and 10 articles — small scale by design
- No user authentication
- No frontend — API only