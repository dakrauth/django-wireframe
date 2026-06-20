import json

from django.db import models
from django.core import exceptions

from wire.logger import logger


class WireLog(models.Model):
    label = models.CharField(max_length=50, db_index=True)
    sub_label = models.CharField(blank=True, max_length=50)
    status = models.CharField(max_length=12, db_index=True)
    data = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def json(self):
        try:
            return json.loads(self.data)
        except Exception:
            logger.exception(f"Could not parse WireLog({self.id}) data as JSON")

        return None

    @json.setter
    def json(self, data):
        try:
            self.data = json.dumps(data)
        except Exception:
            logger.exception(f"Could not marshal WireLog({self.id}) data as JSON")

        self.save()


def wirelog(label, status, sub_label="", data=""):
    sub_label = sub_label[:50]
    if isinstance(data, (dict, tuple, list)):
        data = json.dumps(data)
    else:
        data = str(data)

    return WireLog.objects.create(label=label, status=status, sub_label=sub_label, data=data)


class PrettyJSONField(models.JSONField):
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            json.dumps(value, cls=self.encoder, indent=4)
        except TypeError:
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )
