from typing import Literal
from pydantic import BaseModel, Field


class TGTextEntity(BaseModel):
    type: Literal[
        "plain",
        "bold",
        "italic",
        "strikethrough",
        "blockquote",
        "hashtag",
        "link",
        "phone",
        "pre",
        "spoiler",
        "custom_emoji",
        "text_link",
        "mention",
        "underline",
        "bank_card",
        "code",
        "email",
        "cashtag",  # YES THERE IS SUCH A TYPE
        "bot_command",
        "mention_name",
    ]
    text: str


class TGMessage(BaseModel):
    from_field: str | None = Field(default=None, alias="from")
    text_entities: list[TGTextEntity]


class TGChatDump(BaseModel):
    name: str
    type: Literal[
        "personal_chat",
        "bot_chat",
        "private_group",
        "public_group",
        "private_channel",
        "public_channel",
    ]
    messages: list[TGMessage]
