from enum import Enum
from typing import Optional, List

from pydantic import BaseModel
from telescope_sdk.common import UserFacingDataType
from telescope_sdk.icp import IdealCustomerProfile


class ChatMessageType(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class ChatMessage(BaseModel):
    type: ChatMessageType
    text: str
    sent_at: str


class CampaignStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'ERROR'


class Campaign(UserFacingDataType):
    name: str
    status: CampaignStatus
    sequence_id: Optional[str] = None
    active_icp_id: Optional[str] = None
    outreach_enabled: Optional[bool] = None
    replenish: bool
    icp: IdealCustomerProfile
    icp_chat_history: Optional[List[ChatMessage]] = None
