from dataclasses import dataclass
from datetime import datetime
from typing import Any

from telethon.tl import TLObject


@dataclass
class UserPhoto:
    photo_id: int
    dc_id: int
    has_video: bool
    personal: bool
    stripped_thumb: bytes


@dataclass
class UserOnlineStatus:
    was_online: datetime


@dataclass(frozen=True)
class User(TLObject):
    id: int
    is_self: bool
    contact: bool
    mutual_contact: bool
    deleted: bool
    bot: bool
    bot_chat_history: bool
    bot_nochats: bool
    verified: bool
    restricted: bool
    min: bool
    bot_inline_geo: bool
    support: bool
    scam: bool
    apply_min_photo: bool
    fake: bool
    bot_attach_menu: bool
    premium: bool
    attach_menu_enabled: bool
    bot_can_edit: bool
    close_friend: bool
    stories_hidden: bool
    stories_unavailable: bool
    contact_require_premium: bool
    bot_business: bool
    bot_has_main_app: bool
    bot_forum_view: bool
    bot_forum_can_manage_topics: bool
    bot_can_manage_bots: bool
    bot_guestchat: bool
    bot_guard: bool
    access_hash: int
    first_name: str
    last_name: str
    username: str | None
    phone: str
    photo: UserPhoto
    status: UserOnlineStatus
    bot_info_version: Any | None
    restriction_reason: list
    bot_inline_placeholder: Any | None
    lang_code: Any | None
    emoji_status: Any | None
    usernames: list[str]
    stories_max_id: Any | None
    color: Any | None
    profile_color: Any | None
    bot_active_users: Any | None
    bot_verification_icon: Any | None
    send_paid_messages_stars: Any | None
