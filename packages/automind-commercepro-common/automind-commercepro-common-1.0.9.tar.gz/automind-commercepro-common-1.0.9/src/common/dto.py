from datetime import datetime
from typing import Optional
from unittest.mock import Base
from uuid import UUID
from pydantic import BaseModel, Field, PositiveFloat
from common.utility import get_isoformat


class UserDTO(BaseModel):
    user_id: str | UUID


class TaskDTO(UserDTO):
    id: Optional[int] = None
    start_time: datetime = Field(default_factory=get_isoformat)
    end_time: Optional[datetime | str] = None
    errors: list[dict] = Field(default_factory=list)
    type: str
    name: str
    payload: Optional[dict] = None


class FeedDTO(UserDTO):
    id: Optional[int] = None
    name: str
    public_url: str
    is_active: bool
    description: Optional[str]
    columns: dict
    filters: list[dict]
    modifiers: list[dict]


class AttributeDTO(UserDTO):
    id: Optional[int] = None
    name: str
    type: str


class AttributeValueDTO(UserDTO):
    variant_id: str
    attribute_id: int
    value: str


class BrandDTO(UserDTO):
    id: Optional[int] = None
    name: str


class ListingDTO(UserDTO):
    sku: str
    ean: str
    quantity: int
    price: float
    discount_rate: float
    vat_rate: float


class VariantDTO(UserDTO):
    id: Optional[str | UUID] = None
    product_id: str | UUID
    ean: str
    mpn: Optional[str] = None
    title: Optional[str] = None
    images: Optional[list[str]] = None
    weight_grams: Optional[PositiveFloat] = None
    height_centimeters: Optional[PositiveFloat] = None
    width_centimeters: Optional[PositiveFloat] = None
    depth_centimeters: Optional[PositiveFloat] = None
    raw_specs: Optional[dict] = None
    discount_rate: float = 0.0
    vat_rate: float = 0.22


class OfferDTO(UserDTO):
    id: Optional[int] = None
    price: float
    quantity: int
    supplier_id: int
    variant_id: str | UUID
    supplier_sku: str
    vat_rate: float
    discount_rate: float
    expired_at: Optional[datetime] = None


class OfferPriceDTO(UserDTO):
    variant_id: str | UUID
    offer_id: int
    supplier_id: int
    supplier_sku: str
    offer_price: float
    offer_vat_rate: float
    offer_discount_rate: float
    offer_quantity: int
    price_id: Optional[int]
    price_price: Optional[float]
    price_discount_rate: Optional[float]
    price_vat_rate: Optional[float]
    price_is_locked: Optional[bool]
    supplier_quantity_guard: int
    supplier_is_active: bool


class SupplierScheduleDTO(UserDTO):
    id: Optional[int] = None
    created_at: str
    updated_at: Optional[str]
    supplier_configuration_id: int
    start_time: str
    end_time: Optional[str]
    frequency: int
    is_active: bool


class SupplierConfigurationDTO(UserDTO):
    id: Optional[int] = None
    supplier_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    retriever: str
    retriever_configuration: dict
    mapper: Optional[dict]
    filters: list[dict]
    modifiers: list[dict]


class PriceDTO(UserDTO):
    id: Optional[int] = None
    offer_id: int
    price: float
    vat_rate: float
    discount_rate: float
    is_locked: bool = False
    is_supplier_locked: bool = False


class PriceLockDTO(UserDTO):
    id: Optional[int] = None
    variant_id: str | UUID
    price: float
    discount_rate: float
    vat_rate: float


class SupplierLockDTO(UserDTO):
    supplier_id: int
    variant_id: str | UUID


class SupplierDTO(UserDTO):
    id: Optional[int] = None
    name: str
    min_processing_days: int
    max_processing_days: int
    reliability: str
    is_internal: bool
    is_dropshipper: bool
    is_active: bool
    quantity_guard: int


class TaxonomyDTO(UserDTO):
    id: Optional[int] = None
    path: str


class ProductDTO(UserDTO):
    id: Optional[str] = None
    type: str
    title: Optional[str] = None
    micro_description: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    raw_specs: Optional[dict] = None
    brand_id: Optional[int] = None
    taxonomy_id: Optional[int] = None


class VariantAlignmentRequestDTO(BaseModel):
    """Class to represent a variant alignment."""

    user_id: Optional[str | UUID] = None
    variant_ids: list[str]
