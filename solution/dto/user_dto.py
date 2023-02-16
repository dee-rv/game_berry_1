from datetime import date
from enum import Enum
from typing import List

from pydantic import BaseModel


class Cuisine(str, Enum):
    SouthIndian = "SouthIndian"
    NorthIndian = "NorthIndian"
    Chinese = "Chinese"
    Italian = "Italian"


class Restaurant(BaseModel):
    restaurantId: int
    cuisine: Cuisine
    costBracket: int
    rating: float
    isRecommended: bool
    onboardedTime: date


class CuisineTracking(BaseModel):
    type: str
    noOfOrders: int


class CostTracking(BaseModel):
    type: str
    noOfOrders: int


class User(BaseModel):
    cuisines: List[CuisineTracking]
    costBracket: List[CostTracking]


