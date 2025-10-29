"""
Schemas package for MY_AI_AGENT
Contains Pydantic schemas for data validation
"""

from .product_schema import (
    ProductSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    PRODUCT_FIELDS,
    create_product_document
)

__all__ = [
    'ProductSchema',
    'ProductCreateSchema',
    'ProductUpdateSchema',
    'PRODUCT_FIELDS',
    'create_product_document'
]
