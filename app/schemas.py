from pydantic import BaseModel, Field


class ImageAnalysis(BaseModel):
    product: str
    category: str
    attributes: list[str]
    description: str
    confidence: float = Field(default=0.92, ge=0.0, le=1.0)