"""数据库模型统一导出"""
from app.models.base import TimestampMixin
from app.models.platform_admin import PlatformAdmin
from app.models.institution import Institution
from app.models.org_user import OrgUser
from app.models.class_model import Class
from app.models.student import Student
from app.models.attendance_record import AttendanceRecord

__all__ = [
    "TimestampMixin",
    "PlatformAdmin",
    "Institution",
    "OrgUser",
    "Class",
    "Student",
    "AttendanceRecord",
]
