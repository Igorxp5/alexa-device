import uuid

from typing import List, Dict, Any

from pydantic import BaseModel, Field

def _generate_uuid():
    return str(uuid.uuid4())

class ContextHeader(BaseModel):
    namspace: str
    name: str


class ContextItem(BaseModel):
    header: ContextHeader
    payload: Dict[str, Any]


class EventHeader(BaseModel):
    namspace: str
    name: str
    message_id: str = Field(default_factory=_generate_uuid)
    dialog_request_id: str = Field(default_factory=_generate_uuid)


class EventItem(BaseModel):
    header: EventHeader
    payload: Dict[str, Any]


class Interface(BaseModel):
    context: List[ContextItem]
    event: List[EventItem]
