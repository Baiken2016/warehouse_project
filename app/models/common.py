from sqlalchemy import Column, DateTime
from datetime import datetime
from enum import Enum


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now())


class Status(Enum):
    IN_PROCESS = "in_process"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
