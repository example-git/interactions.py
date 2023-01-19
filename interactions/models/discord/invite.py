from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import attrs

from interactions.client.const import MISSING, Absent
from interactions.client.utils.attr_converters import optional as optional_c
from interactions.client.utils.attr_converters import timestamp_converter
from interactions.models.discord.application import Application
from interactions.models.discord.enums import InviteTargetTypes
from interactions.models.discord.guild import GuildPreview
from interactions.models.discord.snowflake import to_snowflake
from interactions.models.discord.stage_instance import StageInstance
from interactions.models.discord.timestamp import Timestamp

from .base import ClientObject

if TYPE_CHECKING:
    from interactions.client import Client
    from interactions.models import TYPE_GUILD_CHANNEL
    from interactions.models.discord.snowflake import Snowflake_Type
    from interactions.models.discord.user import User

__all__ = ("Invite",)


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class Invite(ClientObject):
    code: str = attrs.field(repr=True)
    """the invite code (unique ID)"""

    # metadata
    uses: int = attrs.field(default=0, repr=True)
    """the guild this invite is for"""
    max_uses: int = attrs.field(repr=False, default=0)
    """max number of times this invite can be used"""
    max_age: int = attrs.field(repr=False, default=0)
    """duration (in seconds) after which the invite expires"""
    created_at: Timestamp = attrs.field(
        default=MISSING, converter=optional_c(timestamp_converter), repr=True
    )
    """when this invite was created"""
    temporary: bool = attrs.field(default=False, repr=True)
    """whether this invite only grants temporary membership"""

    # target data
    target_type: Optional[Union[InviteTargetTypes, int]] = attrs.field(
        default=None, converter=optional_c(InviteTargetTypes), repr=True
    )
    """the type of target for this voice channel invite"""
    approximate_presence_count: Optional[int] = attrs.field(repr=False, default=MISSING)
    """approximate count of online members, returned from the `GET /invites/<code>` endpoint when `with_counts` is `True`"""
    approximate_member_count: Optional[int] = attrs.field(repr=False, default=MISSING)
    """approximate count of total members, returned from the `GET /invites/<code>` endpoint when `with_counts` is `True`"""
    scheduled_event: Optional["Snowflake_Type"] = attrs.field(
        default=None, converter=optional_c(to_snowflake), repr=True
    )
    """guild scheduled event data, only included if `guild_scheduled_event_id` contains a valid guild scheduled event id"""
    expires_at: Optional[Timestamp] = attrs.field(
        default=None, converter=optional_c(timestamp_converter), repr=True
    )
    """the expiration date of this invite, returned from the `GET /invites/<code>` endpoint when `with_expiration` is `True`"""
    stage_instance: Optional[StageInstance] = attrs.field(repr=False, default=None)
    """stage instance data if there is a public Stage instance in the Stage channel this invite is for (deprecated)"""
    target_application: Optional[dict] = attrs.field(repr=False, default=None)
    """the embedded application to open for this voice channel embedded application invite"""
    guild_preview: Optional[GuildPreview] = attrs.field(repr=False, default=MISSING)
    """the guild this invite is for"""

    # internal for props
    _channel_id: "Snowflake_Type" = attrs.field(converter=to_snowflake, repr=True)
    _inviter_id: Optional["Snowflake_Type"] = attrs.field(
        default=None, converter=optional_c(to_snowflake), repr=True
    )
    _target_user_id: Optional["Snowflake_Type"] = attrs.field(
        repr=False, default=None, converter=optional_c(to_snowflake)
    )

    @property
    def channel(self) -> "TYPE_GUILD_CHANNEL":
        """The channel the invite is for."""
        return self._client.cache.get_channel(self._channel_id)

    @property
    def inviter(self) -> Optional["User"]:
        """The user that created the invite or None."""
        return self._client.cache.get_user(self._inviter_id) if self._inviter_id else None

    @property
    def target_user(self) -> Optional["User"]:
        """The user whose stream to display for this voice channel stream invite or None."""
        return self._client.cache.get_user(self._target_user_id) if self._target_user_id else None

    @classmethod
    def _process_dict(cls, data: Dict[str, Any], client: "Client") -> Dict[str, Any]:
        if "stage_instance" in data:
            data["stage_instance"] = StageInstance.from_dict(data, client)

        if "target_application" in data:
            data["target_application"] = Application.from_dict(data, client)

        if "target_event_id" in data:
            data["scheduled_event"] = data["target_event_id"]

        if channel := data.pop("channel", None):
            # invite metadata does not contain enough info to create a channel object
            data["channel_id"] = channel["id"]

        if guild := data.pop("guild", None):
            data["guild_preview"] = GuildPreview.from_dict(guild, client)

        if inviter := data.pop("inviter", None):
            inviter = client.cache.place_user_data(inviter)
            data["inviter_id"] = inviter.id

        return data

    def __str__(self) -> str:
        return self.link

    @property
    def link(self) -> str:
        """The invite link."""
        if self.scheduled_event:
            return f"https://discord.gg/{self.code}?event={self.scheduled_event}"
        return f"https://discord.gg/{self.code}"

    async def delete(self, reason: Absent[str] = MISSING) -> None:
        """
        Delete this invite.

        !!! note
            You must have the `manage_channels` permission on the channel this invite belongs to.

        !!! note
            With `manage_guild` permission, you can delete any invite across the guild.

        Args:
            reason: The reason for the deletion of invite.

        """
        await self._client.http.delete_invite(self.code, reason=reason)
