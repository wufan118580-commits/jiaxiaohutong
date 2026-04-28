"""考勤记录"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    BigInteger, Enum as SAEnum, Numeric, DateTime, ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.models.student import Student
from app.models.institution import Institution


class AttendanceRecord(TimestampMixin):
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("student.id"), nullable=False
    )
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution.id"), nullable=False
    )
    type: Mapped[str] = mapped_column(
        SAEnum("sign_in", "sign_out", name="attendance_type"),
        nullable=False,
        comment="签到/签离",
    )
    method: Mapped[str] = mapped_column(
        SAEnum("face", "manual", name="attendance_method"),
        nullable=False,
        comment="方式",
    )
    face_confidence: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(5, 2), comment="人脸置信度"
    )

    student: Mapped["Student"] = relationship("Student")
    institution: Mapped["Institution"] = relationship("Institution")
