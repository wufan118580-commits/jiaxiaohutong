from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


# ============ 机构注册 / 审核相关 Schema ============

class InstitutionRegisterRequest(BaseModel):
    """机构注册请求"""
    name: str = Field(..., min_length=2, max_length=100)
    contact_person: str = Field(..., min_length=1, max_length=50)
    contact_phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    address: Optional[str] = Field(None, max_length=255)


class InstitutionReviewRequest(BaseModel):
    """审批机构请求"""
    status: int = Field(..., ge=1, le=2)  # 1:通过 2:拒绝
    remark: Optional[str] = None


class InstitutionResponse(BaseModel):
    """机构响应"""
    id: int
    name: str
    contact_person: Optional[str]
    contact_phone: Optional[str]
    address: Optional[str]
    status: int
    face_enabled: bool
    face_expire_date: Optional[date]
    created_at: datetime

    model_config = {"from_attributes": True}


class InstitutionListResponse(BaseModel):
    """机构列表响应（分页）"""
    total: int
    page: int
    page_size: int
    items: list[InstitutionResponse]
