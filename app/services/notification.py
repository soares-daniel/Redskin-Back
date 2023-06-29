import aiohttp

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
    async def send_event_notification(event: EventInResponse, event_operation: EventOperation) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {
                "event_operation": event_operation,
                "event": event
            }
            async with session.post(settings.DISCORD_URL, json=payload) as resp:
                print(resp.status)
                print(await resp.text())

    @staticmethod
    async def send_event_type_notification(event_type: EventTypeInResponse, event_operation: EventOperation) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {
                "event_operation": event_operation,
                "event": event_type
            }
            async with session.post(settings.DISCORD_URL, json=payload) as resp:
                print(resp.status)
                print(await resp.text())

    @staticmethod
    async def send_user_notification(user: UserInResponse, event_operation: EventOperation) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {
                "event_operation": event_operation,
                "event": user
            }
            async with session.post(settings.DISCORD_URL, json=payload) as resp:
                print(resp.status)
                print(await resp.text())

    @staticmethod
    async def send_role_notification(role: RoleInResponse, event_operation: EventOperation) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {
                "event_operation": event_operation,
                "event": role
            }
            async with session.post(settings.DISCORD_URL, json=payload) as resp:
                print(resp.status)
                print(await resp.text())

    @staticmethod
    async def send_user_role_notification(
            user_role: UserRoleInAssign | UserRoleInRemove,
            event_operation: EventOperation
    ) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {
                "event_operation": event_operation,
                "event": user_role
            }
            async with session.post(settings.DISCORD_URL, json=payload) as resp:
                print(resp.status)
                print(await resp.text())

    @staticmethod
    async def send_permission_notification(
            permission: RoleEventTypeInResponse,
            event_operation: EventOperation
    ) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {
                "event_operation": event_operation,
                "event": permission
            }
            async with session.post(settings.DISCORD_URL, json=payload) as resp:
                print(resp.status)
                print(await resp.text())
