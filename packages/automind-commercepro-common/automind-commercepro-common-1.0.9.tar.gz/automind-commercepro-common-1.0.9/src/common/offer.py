import datetime
from typing import Literal, Optional
import uuid
from pydantic import BaseModel, Field
from common.product import Variant
from common.supplier import Supplier
from common.utility import get_isoformat
from common.dto import OfferDTO


class Offer(BaseModel):
    """Represents an offer."""

    id: Optional[int] = None
    price: float
    supplier: Supplier
    variant: Variant
    supplier_sku: str
    quantity: int = 0
    currency: Literal["eur", "usd"] = "eur"
    vat_rate: float = 0.22
    discount_rate: float = 0.0
    max_processing_days: Optional[int] = None
    min_processing_days: Optional[int] = None

    created_at: str = Field(default_factory=get_isoformat)
    expired_at: Optional[datetime.datetime] = None

    def model_dto(self, user_id: uuid.UUID) -> OfferDTO:
        return OfferDTO(
            user_id=str(user_id),
            id=self.id,
            price=self.price,
            quantity=self.quantity,
            supplier_id=self.supplier.id,
            variant_id=self.variant.id,  # type: ignore
            supplier_sku=self.supplier_sku,
            vat_rate=self.vat_rate,
            discount_rate=self.discount_rate,
            expired_at=self.expired_at,
        )
