from typing import Optional
from pydantic import BaseModel, Field
from common.dto import FeedDTO


class Feed(BaseModel):
    id: Optional[int] = None
    name: str
    public_url: str
    is_active: bool
    description: Optional[str] = None
    columns: dict
    filters: list[dict] = Field(default_factory=list)
    modifiers: list[dict] = Field(default_factory=list)

    def model_dto(self, user_id: str) -> FeedDTO:
        return FeedDTO(
            user_id=user_id,
            id=self.id,
            name=self.name,
            public_url=self.public_url,
            is_active=self.is_active,
            description=self.description,
            columns=self.columns,
            filters=self.filters,
            modifiers=self.modifiers,
        )
