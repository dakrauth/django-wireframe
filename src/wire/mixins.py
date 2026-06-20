import uuid
from pathlib import Path

from django.db import models, IntegrityError

from taggit.managers import TaggableManager


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class KeyedMixin(models.Model):
    key = models.CharField(max_length=60, unique=True, editable=False, blank=True)

    class Meta:
        abstract = True

    @staticmethod
    def keyed_file_location(fmt_str):
        if fmt_str.endswith("/"):
            fmt_str = fmt_str[:-1]

        def inner_file_location(instance, filename):
            ext = Path(filename).suffix or ".jpg"
            key = instance.initialized_key()
            return f"{fmt_str}/{key}{ext}"

        return inner_file_location

    def initialized_key(self):
        if not self.key:
            u = uuid.uuid4()
            self.key = f"{u.time_low:x}"

        return self.key

    def save(self, *args, **kwargs):
        try:
            self.initialized_key()
            return super().save(*args, **kwargs)
        except IntegrityError as exc:
            msg = str(exc)
            if "Duplicate" in msg and f"{self._meta.db_table}.key" in msg:
                self.key = None
                self.initialized_key()
                return super().save(*args, **kwargs)
            raise


class TaggedMixin(models.Model):
    tags = TaggableManager(blank=True)

    class Meta:
        abstract = True


class BaseMixin(TimeStampMixin, KeyedMixin, TaggedMixin):
    class Meta:
        abstract = True
