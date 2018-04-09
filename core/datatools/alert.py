import time

from typing import List, Type

from core import consts
from core import models
from core.datatools.alert_handlers.base_handler import BaseHandler

from project import settings


class Alert:
    def run(self):
        while True:
            for handler in self.get_handlers():
                self.pull_handlers(handler)
            time.sleep(settings.ALERT_DELAY * 100)

    def pull_handlers(self, handler_class: Type[BaseHandler]=None):
        templates = self.get_templates_for_alert()
        handler = handler_class(templates)
        handler.start_alert()

    @staticmethod
    def get_handlers() -> List:
        handlers = []
        for handler_import_path in settings.ALERT_HANDLERS:
            handler = __import__(handler_import_path)
            handlers.append(handler)

        return handlers

    @staticmethod
    def get_templates_for_alert() -> List[models.TaskTemplate]:
        tasks_templates_fail = []
        tasks_templates = models.TaskTemplate.objects.all()

        for tasks_template in tasks_templates:
            if tasks_template.tasks.last().status == consts.FAIL:
                tasks_templates_fail.append(tasks_template)

        return tasks_templates_fail
