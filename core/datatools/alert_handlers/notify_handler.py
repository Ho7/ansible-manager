import datetime
import notify.client

from django.conf import settings
from core.datatools.alert_handlers.base_handler import BaseHandler
from core import models

from typing import List, Dict


class NotifyClient(notify.client.NotifyClient):
    def get_service_url(self):
        return settings.NOTIFY_SERVICE_URL


class AlertUser:
    phone = None
    days = None
    hour = None
    minute = None

    def __init__(self, phone: str, days: tuple, hour: int, minute: int):
        self.phone = phone
        self.days = days
        self.hour = hour
        self.minute = minute

    def need_alert(self) -> bool:
        now = datetime.datetime.now()

        alert_day = now.day in self.days
        alert_hour = now.hour == self.hour
        alert_minute = now.time().minute == self.minute or now.time().minute + settings.ALERT_DELAY > self.minute

        return alert_day and alert_hour and alert_minute

    @classmethod
    def get_all_users(cls) -> List:
        conf = cls.get_conf()
        users = []
        for user in conf:
            user.append(cls(**user))
        return users

    @staticmethod
    def get_conf() -> List:
        return settings.ALERT_USERS.values()


class NotifyHandler(BaseHandler):

    def start_alert(self):
        notify_client = self.get_notify_client()

        for alert_user in self.get_alert_users():
            if alert_user.need_alert():
                notify_client.create_call(
                    message=self.prepare_data['message'], phone_numbers=[alert_user.phone, ],
                )

    @staticmethod
    def get_alert_users() -> List[AlertUser]:
        return AlertUser.get_all_users()

    @staticmethod
    def preparation_data(templates: List[models.TaskTemplate]) -> Dict:
        template_name = []

        for template in templates:
            template_name.append(str(template.name))

        prepare_data = {
            'message': 'Шаблоны задач с именами {name} имеют статус FAIL'.format(name=', '.join(template_name))
        }

        return prepare_data

    @staticmethod
    def get_notify_client() -> NotifyClient:
        return NotifyClient(
            auth_token=settings.NOTIFY_SERVICE_TOKEN,
        )
