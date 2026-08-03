"""
Book data model.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Book:
    """
    Represents a cleaned book record.
    """

    title: str
    category_name: str
    price_gbp: float
    rating: int
    in_stock: bool
    price_inr: Optional[float] = None