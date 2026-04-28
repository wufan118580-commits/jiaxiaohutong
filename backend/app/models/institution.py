"""机构表（机构注册/审核）"""
from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, SmallInteger, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampMixin


class Institution(TimestampMixin):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_person: Mapped[Optional[str]] = mapped_column(String(50))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[int] = mapped_column(
        SmallInteger, default=0, comment="0:待审核 1:已通过 2:已拒绝"
    )
    face_enabled: Mapped[bool] = mapped_column(
        SmallInteger, default=0, comment="人脸打卡功能开关"
    )
    face_expire_date: Mapped[Optional[date]] = mapped_column(
        Date, comment="人脸功能到期时间"
    )
