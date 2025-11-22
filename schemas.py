"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Review(BaseModel):
    """
    Client reviews for JP Creation
    Collection name: "review"
    """
    name: str = Field(..., min_length=2, max_length=80, description="Reviewer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating (1-5)")
    message: str = Field(..., min_length=5, max_length=1000, description="Review text")
    event_type: Optional[str] = Field(None, max_length=60, description="Optional: Wedding / Sangeet / Reception / etc.")
    instagram: Optional[str] = Field(None, max_length=80, description="Optional Instagram handle of reviewer")
