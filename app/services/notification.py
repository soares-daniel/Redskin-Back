import aiohttp

from app.services.base import BaseService
from app.config.manager import settings
from app.models.db.event import Event
from app.models.schemas.event import EventInResponse
from app.models.schemas.event_operation import EventOperation


class NotificationService(BaseService):
    @staticmethod
    async def send_event_notification(event: Event, event_operation: EventOperation) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {
                "event_operation": event_operation,
                "event": EventInResponse.from_orm(event)
            }
            async with session.post(settings.DISCORD_URL, json=payload) as resp:
                print(resp.status)
                print(await resp.text())
