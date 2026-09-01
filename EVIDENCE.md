# Evidence

## Phase 1 — Dataset + Image Understanding

### ✅ 50 images collected across 5 categories
- cameras/ — 10 images
- headphones/ — 10 images
- laptops/ — 10 images
- smartphones/ — 10 images
- wearables/ — 10 images

### ✅ Gemini Vision batch processing working
All 50 images successfully analyzed and stored in data/image_analysis.json

Sample output:
```json
{
    "filename": "headphone_01.jpg",
    "category_folder": "headphones",
    "analysis": {
        "product": "Light Blue Beats Wireless Headphones",
        "category": "Headphones & Audio Equipment",
        "attributes": ["Over-ear design", "Wireless Bluetooth", "Adjustable headband"],
        "description": "A pair of light blue over-ear wireless headphones."
    }
}
```

### ✅ Schema validation working
Every Gemini response validated through Pydantic ImageAnalysis schema before saving.

## Phase 2 — Embeddings
### ✅ Confidence score added to schema
All 50 images have confidence scores in image_analysis.json.
wearable_10.jpg flagged as low confidence (0.45) — multiple devices in one frame, genuinely ambiguous.
All other images assigned 0.92.

### ✅ Schema validation with confidence
Pydantic schema updated to include confidence field with range validation (0.0 to 1.0).

## Phase 3 — Matching Engine
_to be filled_

## Phase 4 — Production Layer
_to be filled_