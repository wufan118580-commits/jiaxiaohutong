"""机构注册与审核 - 业务逻辑层"""
from typing import Optional
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.institution import Institution
from app.models.org_user import OrgUser
from app.core.auth import hash_password
from app.schemas.institution import InstitutionRegisterRequest, InstitutionReviewRequest


async def create_institution(
    db: AsyncSession,
    data: InstitutionRegisterRequest,
) -> Institution:
    """提交机构注册申请（status=0 待审核）"""
    institution = Institution(
        name=data.name,
        contact_person=data.contact_person,
        contact_phone=data.contact_phone,
        address=data.address,
        status=0,  # 待审核
        face_enabled=False,
    )
    db.add(institution)
    await db.flush()
    await db.refresh(institution)
    return institution


async def get_institutions(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    keyword: Optional[str] = None,
    status: Optional[int] = None,
) -> tuple[list[Institution], int]:
    """分页查询机构列表（平台管理员用）"""
    query = select(Institution).where(Institution.is_delete == False)

    count_query = select(func.count()).select_from(Institution).where(Institution.is_delete == False)

    if keyword:
        kw_filter = Institution.name.like(f"%{keyword}%")
        query = query.where(kw_filter)
        count_query = count_query.where(kw_filter)

    if status is not None:
        query = query.where(Institution.status == status)
        count_query = count_query.where(Institution.status == status)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    offset_val = (page - 1) * page_size
    query = (
        query.order_by(Institution.id.desc())
        .offset(offset_val)
        .limit(page_size)
    )
    result = await db.execute(query)
    items = result.scalars().all()

    return list(items), total


async def get_institution_by_id(db: AsyncSession, institution_id: int) -> Optional[Institution]:
    """根据ID查询单个机构"""
    result = await db.execute(
        select(Institution).where(
            Institution.id == institution_id,
            Institution.is_delete == False,
        )
    )
    return result.scalar_one_or_none()


async def review_institution(
    db: AsyncSession,
    institution_id: int,
    data: InstitutionReviewRequest,
) -> Institution:
    """审核机构：通过时自动生成 principal 账号"""
    institution = await get_institution_by_id(db, institution_id)
    if not institution:
        raise ValueError("机构不存在")

    if institution.status != 0:
        raise ValueError("该机构已审核，不可重复操作")

    institution.status = data.status

    # 通过 → 自动创建校长账号（默认密码手机后4位）
    if data.status == 1:
        phone = institution.contact_phone or "00000000000"
        default_pwd = phone[-4:]
        principal = OrgUser(
            institution_id=institution_id,
            name=institution.contact_person or institution.name,
            phone=phone,
            password_hash=hash_password(default_pwd),
            role="principal",
        )
        db.add(principal)

    await db.flush()
    await db.refresh(institution)
    return institution
