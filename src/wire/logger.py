from django.conf import settings
import logging

wire_logger_root = getattr(settings, "WIRE_LOGGER", "wire")
logger = logging.getLogger(wire_logger_root)


def getLogger(name):
    return logging.getLogger(f"{wire_logger_root}.name")
