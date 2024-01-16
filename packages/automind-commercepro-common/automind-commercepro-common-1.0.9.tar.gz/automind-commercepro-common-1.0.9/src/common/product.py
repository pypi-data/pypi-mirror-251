import re
from typing import Literal, Optional, List
from pydantic import PositiveFloat, field_validator, BaseModel
from uuid import UUID
from common.dto import (
    AttributeDTO,
    AttributeValueDTO,
    BrandDTO,
    ProductDTO,
    TaxonomyDTO,
    VariantDTO,
)


class Brand(BaseModel):
    """Represents a Brand."""

    id: Optional[int] = None
    name: str

    def model_dto(self, user_id: UUID) -> BrandDTO:
        return BrandDTO(
            user_id=str(user_id),
            id=self.id,
            name=self.name,
        )


class Taxonomy(BaseModel):
    """Represents a Taxonomy."""

    id: Optional[int] = None
    path: str

    def model_dto(self, user_id: UUID) -> TaxonomyDTO:
        return TaxonomyDTO(
            id=self.id,
            user_id=str(user_id),
            path=self.path,
        )


class Product(BaseModel):
    """Common data between a Simple and a Variant product."""

    id: Optional[UUID] = None
    type: Literal["simple", "variant"] = "simple"
    brand: Optional[Brand] = None
    title: Optional[str] = None
    micro_description: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    taxonomy: Optional[Taxonomy] = None
    raw_specs: Optional[dict] = None

    def model_dto(self, user_id: UUID) -> ProductDTO:
        return ProductDTO(
            user_id=str(user_id),
            id=str(self.id),
            type=self.type,
            title=self.title,
            micro_description=self.micro_description,
            short_description=self.short_description,
            long_description=self.long_description,
            raw_specs=self.raw_specs,
            brand_id=self.brand.id if self.brand else None,
            taxonomy_id=self.taxonomy.id if self.taxonomy else None,
        )


class Attribute(BaseModel):
    """Represents a Product Attribute."""

    id: Optional[int] = None
    name: str
    type: Literal["string", "integer", "float"]

    def model_dto(self, user_id: UUID) -> AttributeDTO:
        return AttributeDTO(
            user_id=str(user_id),
            id=self.id,
            name=self.name,
            type=self.type,
        )


class AttributeValue(BaseModel):
    """Represents a Product Attribute Value."""

    variant_id: Optional[UUID] = None
    value: str | int | float
    attribute: Attribute

    def model_dto(self, user_id: UUID) -> AttributeValueDTO:
        return AttributeValueDTO(
            user_id=str(user_id),
            variant_id=self.variant_id,  # type: ignore
            value=str(self.value),
            attribute_id=self.attribute.id,  # type: ignore
        )


class Variant(BaseModel):
    """Variant-specific data linked to a parent `Product`."""

    id: Optional[UUID] = None
    product: Product
    ean: str
    mpn: Optional[str] = None
    title: Optional[str] = None
    images: Optional[List[str]] = None
    weight_grams: Optional[PositiveFloat] = None
    height_centimeters: Optional[PositiveFloat] = None
    width_centimeters: Optional[PositiveFloat] = None
    depth_centimeters: Optional[PositiveFloat] = None
    attributes: Optional[list[AttributeValue]] = None
    raw_specs: Optional[dict] = None
    discount_rate: float = 0.0
    vat_rate: float = 0.22

    def get_search_string(self) -> str:
        """"""
        search_string = ""
        if self.title:
            search_string += self.title
        if self.product.title:
            search_string += self.product.title
        if self.mpn:
            search_string += " " + self.mpn
        if self.ean:
            search_string += " " + self.ean
        if self.product.id:
            search_string += " " + str(self.product.id)
        if self.product.taxonomy:
            search_string += " " + self.product.taxonomy.path
        return search_string

    @field_validator("ean")
    @classmethod
    def ean_must_be_valid(cls, v):
        """Validates the EAN."""

        digit_regex = r"^\d{13}$"
        if not re.match(digit_regex, v):
            raise ValueError("Invalid EAN.")
        return v

    def model_dto(self, user_id: UUID) -> VariantDTO:
        return VariantDTO(
            user_id=str(user_id),
            id=str(self.id),
            product_id=str(self.product.id),  # type: ignore
            ean=self.ean,
            mpn=self.mpn,
            title=self.title,
            images=self.images,
            weight_grams=self.weight_grams,
            height_centimeters=self.height_centimeters,
            width_centimeters=self.width_centimeters,
            depth_centimeters=self.depth_centimeters,
            raw_specs=self.raw_specs,
            discount_rate=self.discount_rate,
            vat_rate=self.vat_rate,
        )
