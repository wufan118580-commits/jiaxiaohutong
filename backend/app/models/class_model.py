"""班级"""
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.models.institution import Institution


class Class(TimestampMixin):
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    institution: Mapped["Institution"] = relationship("Institution")

    students: Mapped[list["Student"]] = relationship(
        "Student", back_populates="class_"
    )
