import uuid
from pydantic import BaseModel, Field
from common.offer import Offer
from common.utility import get_isoformat
from typing import Any, Optional

from src.common.dto import PriceDTO


class Price(BaseModel):
    """Represents a price."""

    id: Optional[int] = None
    price: float
    offer: Offer
    is_locked: bool = False
    vat_rate: float = 0.22
    discount_rate: float = 0.0

    created_at: str = Field(default_factory=get_isoformat)
    expired_at: Optional[str] = None
    is_supplier_locked: bool = False

    def model_dto(self, user_id: uuid.UUID) -> PriceDTO:
        return PriceDTO(
            user_id=str(user_id),
            id=self.id,
            offer_id=self.offer.id,  # type: ignore
            price=self.price,
            vat_rate=self.vat_rate,
            discount_rate=self.discount_rate,
            is_locked=self.is_locked,
            is_supplier_locked=self.is_supplier_locked,
        )
