"""机构用户（校长/老师）"""
import json
from typing import Optional
from sqlalchemy import String, BigInteger, Enum as SAEnum, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.models.institution import Institution


class OrgUser(TimestampMixin):
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        SAEnum("principal", "teacher", name="org_user_role"),
        default="teacher",
        nullable=False,
    )
    permissions: Mapped[Optional[dict | list]] = mapped_column(
        JSON, comment="教师权限配置"
    )

    institution: Mapped["Institution"] = relationship("Institution")
