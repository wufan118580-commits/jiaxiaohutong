"""机构注册与审核 API 路由"""
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.response import success_response, error_response, ResponseCode
from app.core.auth import require_roles
from app.schemas.institution import (
    InstitutionRegisterRequest,
    InstitutionReviewRequest,
    InstitutionListResponse,
    InstitutionResponse,
)
from app.services import institution_service

router = APIRouter(prefix="/platform/institutions", tags=["平台-机构管理"])


@router.post("/", summary="提交机构注册申请（无需认证）")
async def register_institution(
    body: InstitutionRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        institution = await institution_service.create_institution(db, body)
        return success_response(data={"id": institution.id}, msg="注册成功，请等待审核")
    except Exception as e:
        return error_response(code=ResponseCode.SERVER_ERROR, msg=str(e))


@router.get(
    "/",
    summary="查看机构列表（需平台管理员）",
    dependencies=[Depends(require_roles("platform_admin"))],
)
async def list_institutions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str = Query("", max_length=50),
    status: int | None = Query(None, ge=0, le=2),
    db: AsyncSession = Depends(get_db),
):
    items, total = await institution_service.get_institutions(
        db, page=page, page_size=page_size, keyword=keyword or None, status=status
    )

    resp = InstitutionListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[InstitutionResponse.model_validate(it) for it in items],
    )
    return success_response(data=resp.model_dump())


@router.put(
    "/{institution_id}/review",
    summary="审批机构（需平台管理员）",
    dependencies=[Depends(require_roles("platform_admin"))],
)
async def review_institution(
    institution_id: int,
    body: InstitutionReviewRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        institution = await institution_service.review_institution(db, institution_id, body)
        status_text = {1: "已通过", 2: "已拒绝"}.get(body.status, "")
        msg = f"审核{status_text}"
        if body.status == 1:
            msg += "，校长账号已自动创建"
        return success_response(
            data={"id": institution.id, "status": institution.status},
            msg=msg,
        )
    except ValueError as e:
        return error_response(code=ResponseCode.PARAM_ERROR, msg=str(e))
    except Exception as e:
        return error_response(code=ResponseCode.SERVER_ERROR, msg=str(e))
