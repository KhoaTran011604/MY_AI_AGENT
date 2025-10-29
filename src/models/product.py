"""
Product Schema using Pydantic
Defines product data structure with validation
Compatible with PyMongo
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId


class ProductSchema(BaseModel):
    """
    Product schema with Pydantic validation

    This schema provides:
    - Type validation
    - Field constraints
    - JSON serialization
    - Compatible with PyMongo dict format
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    # MongoDB ID (optional for creation)
    id: Optional[Any] = Field(default=None, alias="_id")

    # Required fields
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: str = Field(..., min_length=1, description="Product description")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")
    brand: str = Field(..., min_length=1, max_length=100, description="Brand name")
    price: float = Field(..., gt=0, description="Product price (must be positive)")

    # Optional fields with defaults
    currency: str = Field(default="VND", max_length=10, description="Currency code")
    stock: int = Field(default=0, ge=0, description="Available stock (non-negative)")
    rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Product rating (0-5)")

    # Complex fields
    specifications: Dict[str, Any] = Field(default_factory=dict, description="Product specifications")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    tags: List[str] = Field(default_factory=list, description="Product tags")

    # Embedding for RAG system
    embedding: Optional[List[float]] = Field(default=None, description="Vector embedding")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Validate tags - max 50 chars each"""
        for tag in v:
            if len(tag) > 50:
                raise ValueError(f"Tag '{tag}' exceeds 50 characters")
        return v

    @field_validator('images')
    @classmethod
    def validate_images(cls, v: List[str]) -> List[str]:
        """Validate image URLs"""
        # Could add URL validation here if needed
        return v

    def to_mongo_dict(self) -> Dict[str, Any]:
        """
        Convert to MongoDB-compatible dictionary

        Returns:
            dict: Dictionary ready for MongoDB insertion/update
        """
        data = self.model_dump(by_alias=True, exclude_none=True)

        # Remove _id if it's None (for new documents)
        if data.get('_id') is None:
            data.pop('_id', None)

        return data

    @classmethod
    def from_mongo_dict(cls, data: Dict[str, Any]) -> 'ProductSchema':
        """
        Create ProductSchema from MongoDB document

        Args:
            data: MongoDB document dictionary

        Returns:
            ProductSchema: Validated product schema instance
        """
        return cls(**data)

    def is_in_stock(self) -> bool:
        """Check if product is in stock"""
        return self.stock > 0

    def format_price(self) -> str:
        """Format price for display"""
        if self.currency == "VND":
            return f"{self.price:,.0f}đ"
        return f"{self.price:,.2f} {self.currency}"


class ProductCreateSchema(BaseModel):
    """Schema for creating new products (without ID and timestamps)"""

    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    brand: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    currency: str = Field(default="VND", max_length=10)
    stock: int = Field(default=0, ge=0)
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    specifications: Dict[str, Any] = Field(default_factory=dict)
    images: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class ProductUpdateSchema(BaseModel):
    """Schema for updating existing products (all fields optional)"""

    model_config = ConfigDict(extra='forbid')  # Prevent unknown fields

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=10)
    stock: Optional[int] = Field(None, ge=0)
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    specifications: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None


# Field descriptions for documentation
PRODUCT_FIELDS = {
    "name": "Product name (required, string, 1-200 chars)",
    "description": "Product description (required, string)",
    "category": "Product category (required, string, 1-100 chars)",
    "brand": "Brand name (required, string, 1-100 chars)",
    "price": "Product price (required, float, > 0)",
    "currency": "Currency code (optional, string, default: VND)",
    "stock": "Available stock (optional, int, default: 0, >= 0)",
    "rating": "Product rating (optional, float, 0.0-5.0, default: 0.0)",
    "specifications": "Product specifications (optional, dict)",
    "images": "Product image URLs (optional, list of strings)",
    "tags": "Product tags (optional, list of strings, max 50 chars each)",
    "created_at": "Creation timestamp (auto-generated)",
    "updated_at": "Last update timestamp (auto-updated)",
    "embedding": "Vector embedding for RAG (optional, list of floats)"
}


# Helper function to create product document
def create_product_document(
    name: str,
    description: str,
    category: str,
    brand: str,
    price: float,
    currency: str = "VND",
    stock: int = 0,
    specifications: Optional[Dict] = None,
    images: Optional[List[str]] = None,
    rating: float = 0.0,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create and validate a product document

    Args:
        name: Product name
        description: Product description
        category: Product category
        brand: Brand name
        price: Product price
        currency: Currency code (default: VND)
        stock: Available stock (default: 0)
        specifications: Product specifications
        images: Image URLs
        rating: Product rating (0-5)
        tags: Product tags

    Returns:
        dict: Validated product document ready for MongoDB

    Raises:
        ValidationError: If validation fails
    """
    product = ProductSchema(
        name=name,
        description=description,
        category=category,
        brand=brand,
        price=price,
        currency=currency,
        stock=stock,
        specifications=specifications or {},
        images=images or [],
        rating=rating,
        tags=tags or [],
        embedding=None
    )

    return product.to_mongo_dict()
