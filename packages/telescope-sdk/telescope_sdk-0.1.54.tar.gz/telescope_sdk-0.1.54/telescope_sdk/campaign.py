from enum import Enum
from typing import Optional, List

from pydantic import BaseModel
from telescope_sdk.common import UserFacingDataType


class ChatMessageType(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class ChatMessage(BaseModel):
    type: ChatMessageType
    text: str
    sent_at: str


class OutreachStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'DISABLED'


class Campaign(UserFacingDataType):
    name: str
    outreach_status: OutreachStatus
    sequence_id: Optional[str] = None
    active_icp_id: Optional[str] = None
    outreach_enabled: Optional[bool] = None
    icp_chat_history: Optional[List[ChatMessage]] = None
    icp_chat_enabled: bool = False
