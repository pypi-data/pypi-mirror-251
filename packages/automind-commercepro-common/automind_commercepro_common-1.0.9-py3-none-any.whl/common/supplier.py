from datetime import datetime
from time import time
from tracemalloc import start
from typing import Literal, Optional
import uuid
from pydantic import BaseModel, Field, PositiveInt
from common.dto import SupplierDTO, SupplierConfigurationDTO, SupplierScheduleDTO
from common.utility import get_isoformat


class SupplierSchedule(BaseModel):
    id: Optional[int] = None
    created_at: datetime = Field(default_factory=get_isoformat)
    updated_at: Optional[datetime] = None
    supplier_configuration_id: int
    start_time: str
    end_time: Optional[str]
    frequency: PositiveInt
    is_active: bool = False

    def model_dto(self, user_id: uuid.UUID) -> SupplierScheduleDTO:
        return SupplierScheduleDTO(
            user_id=user_id,
            id=self.id,
            created_at=str(self.created_at),
            updated_at=str(self.updated_at),
            supplier_configuration_id=self.supplier_configuration_id,
            start_time=self.start_time,
            end_time=self.end_time,
            frequency=self.frequency,
            is_active=self.is_active,
        )


class SupplierConfiguration(BaseModel):
    id: Optional[int] = None
    user_id: uuid.UUID
    supplier_id: int
    created_at: datetime = Field(default_factory=get_isoformat)
    updated_at: Optional[datetime] = None
    retriever: str
    retriever_configuration: dict
    mapper: Optional[dict] = None
    filters: list[dict] = Field(default_factory=list)
    modifiers: list[dict] = Field(default_factory=list)

    def model_dto(self) -> SupplierConfigurationDTO:
        return SupplierConfigurationDTO(
            user_id=self.user_id,
            id=self.id,
            supplier_id=self.supplier_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            retriever=self.retriever,
            retriever_configuration=self.retriever_configuration,
            mapper=self.mapper,
            filters=self.filters,
            modifiers=self.modifiers,
        )


class Supplier(BaseModel):
    id: Optional[int] = None
    name: str
    min_processing_days: int = 3
    max_processing_days: int = 5
    reliability: Literal["high", "medium", "low"] = "medium"
    is_internal: bool = False
    is_dropshipper: bool = False
    is_active: bool = False
    quantity_guard: int = 0

    def model_dto(self, user_id: uuid.UUID) -> SupplierDTO:
        return SupplierDTO(
            user_id=user_id,
            id=self.id,
            name=self.name,
            min_processing_days=self.min_processing_days,
            max_processing_days=self.max_processing_days,
            reliability=self.reliability,
            is_internal=self.is_internal,
            is_dropshipper=self.is_dropshipper,
            is_active=self.is_active,
            quantity_guard=self.quantity_guard,
        )


class SupplierOffer(BaseModel):
    """Represents a lightweight `Supplier` offer."""

    sku: str
    ean: Optional[str] = None
    mpn: Optional[str] = None
    title: Optional[str] = None
    brand_name: Optional[str] = None
    price: float
    quantity: int = 0
    discount_rate: float = 0.0
    images: Optional[list[str]] = None
    vat_rate: float = 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SupplierOffer):
            return False

        return (
            self.sku == other.sku
            and self.price == other.price
            and self.quantity == other.quantity
            and self.discount_rate == other.discount_rate
            and self.vat_rate == other.vat_rate
        )
