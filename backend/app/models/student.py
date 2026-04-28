"""学员"""
from typing import Optional
from sqlalchemy import String, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampMixin
from app.models.institution import Institution
from app.models.class_model import Class


class Student(TimestampMixin):
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution.id"), nullable=False
    )
    class_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("class.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[Optional[int]] = mapped_column(SmallInteger, comment="性别")
    face_image_url: Mapped[Optional[str]] = mapped_column(
        String(255), comment="COS人脸照片URL"
    )
    parent_phone: Mapped[Optional[str]] = mapped_column(
        String(20), comment="关联家长端账号"
    )
    status: Mapped[int] = mapped_column(
        SmallInteger, default=1, comment="1:在学 0:离校"
    )

    institution: Mapped["Institution"] = relationship("Institution")
    class_: Mapped[Optional["Class"]] = relationship("Class", back_populates="students")
