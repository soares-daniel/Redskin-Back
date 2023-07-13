import aiohttp
from aiohttp import ServerDisconnectedError

from app.models.schemas.event_type import EventTypeInResponse
from app.models.schemas.role import RoleInResponse
from app.models.schemas.role_event_type import RoleEventTypeInResponse
from app.models.schemas.user import UserInResponse
from app.models.schemas.user_role import UserRoleInAssign, UserRoleInRemove
from app.services.base import BaseService
from app.config.manager import settings
from app.models.schemas.event import EventInResponse
from app.models.schemas.event_operation import EventOperation


class NotificationService(BaseService):
    @staticmethod
    async def send_notification(
            url: str,
            payload: dict
    ) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    print(resp.status)
                    print(await resp.text())
        except ServerDisconnectedError:
            print("Server disconnected")

    async def send_event_notification(
            self,
            event: EventInResponse,
            event_operation: EventOperation
    ) -> None:
        payload = {
            "event_operation": event_operation.value,
            "event": event.json()
        }
        await self.send_notification(settings.DISCORD_URL, payload)

    async def send_event_type_notification(
            self,
            event_type: EventTypeInResponse,
            event_operation: EventOperation
    ) -> None:
        payload = {
            "event_operation": event_operation.value,
            "event": event_type.json()
        }
        await self.send_notification(settings.DISCORD_URL, payload)

    async def send_user_notification(
            self,
            user: UserInResponse,
            event_operation: EventOperation
    ) -> None:
        payload = {
            "event_operation": event_operation.value,
            "event": user.json()
        }
        await self.send_notification(settings.DISCORD_URL, payload)

    async def send_role_notification(
            self,
            role: RoleInResponse,
            event_operation: EventOperation
    ) -> None:
        payload = {
            "event_operation": event_operation.value,
            "event": role.json()
        }
        await self.send_notification(settings.DISCORD_URL, payload)

    async def send_user_role_notification(
            self,
            user_role: UserRoleInAssign | UserRoleInRemove,
            event_operation: EventOperation
    ) -> None:
        payload = {
            "event_operation": event_operation.value,
            "event": user_role.json()
        }
        await self.send_notification(settings.DISCORD_URL, payload)

    async def send_permission_notification(
            self,
            permission: RoleEventTypeInResponse,
            event_operation: EventOperation
    ) -> None:
        payload = {
            "event_operation": event_operation.value,
            "event": permission.json()
        }
        await self.send_notification(settings.DISCORD_URL, payload)
