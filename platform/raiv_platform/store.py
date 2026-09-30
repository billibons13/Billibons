"""Minimal in-memory data model shared by agents (swap for a database later)."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product:
    id: str
    name: str
    price_eur: float           # per unit below
    unit: str                  # "100g", "kg", "pcs"
    stock: float               # in the same unit
    min_stock: float = 0
    photo_url: str = ""


@dataclass
class OrderLine:
    product_id: str
    qty: float                 # in product units


@dataclass
class Order:
    id: str
    shop_id: str
    customer_id: str
    lines: list
    total_eur: float
    created_at: datetime
    city: str = ""
    address: str = ""
    phone: str = ""


@dataclass
class Customer:
    id: str
    name: str
    phone: str = ""


@dataclass
class Store:
    products: dict = field(default_factory=dict)
    orders: list = field(default_factory=list)
    customers: dict = field(default_factory=dict)
