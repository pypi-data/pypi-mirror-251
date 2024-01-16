import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field
from common.dto import TaskDTO
from common.utility import get_isoformat


class Task(BaseModel):
    """Represents a Task."""

    id: Optional[int] = None
    start_time: datetime.datetime = Field(default_factory=get_isoformat)
    end_time: Optional[datetime.datetime] = None
    errors: Optional[list[dict]] = None
    type: str
    name: str
    payload: Optional[dict] = None

    def model_dto(self, user_id: uuid.UUID) -> TaskDTO:
        return TaskDTO(
            user_id=str(user_id),
            id=self.id,
            start_time=self.start_time,
            end_time=self.end_time,
            errors=self.errors,
            type=self.type,
            payload=self.payload,
            name=self.name,
        )
