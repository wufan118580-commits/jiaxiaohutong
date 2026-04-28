from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """通用字段：id / created_at / is_delete + 软删除过滤"""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    is_delete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def soft_delete(self):
        self.is_delete = True
