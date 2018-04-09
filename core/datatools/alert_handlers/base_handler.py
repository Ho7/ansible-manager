from typing import Dict, Type
from core import models


class BaseHandler:
    def __init__(self, templates: Type[models.TaskTemplate]):

        assert templates is not None

        self.templates = templates
        self.prepare_data = self.preparation_data(templates)

    def start_alert(self):
        pass

    @staticmethod
    def preparation_data(templates: Type[models.TaskTemplate]) -> Dict:
        prepare_data = {}
        return prepare_data
