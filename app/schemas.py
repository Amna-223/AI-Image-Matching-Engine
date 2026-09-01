from pydantic import BaseModel

class ImageAnalysis(BaseModel):
    product: str
    category: str
    attributes: list[str]
    description: str