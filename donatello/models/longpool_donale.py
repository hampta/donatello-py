from __future__ import annotations

from datetime import datetime as Datetime
from typing import Dict, Union

from pydantic import BaseModel, Field, validator


class LongpoolDonate(BaseModel):
    client_name: str = Field(alias="clientName")
    message: str = Field(alias="message")
    amount: str = Field(alias="amount")
    currency: str = Field(alias="currency")
    source: str = Field(alias="source")
    image: str = Field(alias="image")
    sound: str = Field(alias="sound")
    video: str = Field(alias="video")
    interaction_media: str = Field(alias="interactionMedia")
    interaction_media_start_time: str = Field(alias="interactionMediaStartTime")
    goal_widget_name: str = Field(alias="goalWidgetName")
    manually_approved: bool = Field(alias="manuallyApproved")
    ban: bool = Field(alias="ban")
    is_published: bool = Field(alias="isPublished")
    created_at: Datetime = Field(alias="createdAt")
    is_subscription: bool = Field(alias="isSubscription")
    uploaded_voice: str = Field(alias="uploadedVoice")
    name: str = Field(alias="name")

    @validator("created_at", pre=True)
    def validate_created_at(cls, value) -> Datetime:
        return Datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"<LongpoolDonate client_name={self.client_name} message={self.message} amount={self.amount} currency={self.currency} source={self.source} image={self.image} sound={self.sound} video={self.video} interaction_media={self.interaction_media} interaction_media_start_time={self.interaction_media_start_time} goal_widget_name={self.goal_widget_name} manually_approved={self.manually_approved} ban={self.ban} is_published={self.is_published} created_at={self.created_at} is_subscription={self.is_subscription} uploaded_voice={self.uploaded_voice} name={self.name}>"

    def __repr__(self) -> Dict[str, Union[str, int, bool, Datetime]]:
        return f"<LongpoolDonate client_name={self.client_name} message={self.message} amount={self.amount} currency={self.currency} source={self.source} image={self.image} sound={self.sound} video={self.video} interaction_media={self.interaction_media} interaction_media_start_time={self.interaction_media_start_time} goal_widget_name={self.goal_widget_name} manually_approved={self.manually_approved} ban={self.ban} is_published={self.is_published} created_at={self.created_at} is_subscription={self.is_subscription} uploaded_voice={self.uploaded_voice} name={self.name}>"

    def __lt__(self: LongpoolDonate, other: LongpoolDonate) -> bool:
        return self.amount < other.amount