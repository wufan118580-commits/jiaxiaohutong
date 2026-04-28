"""健康检查接口"""
from fastapi import APIRouter
from datetime import datetime

from app.core.response import success_response

router = APIRouter()


@router.get("/health")
async def health_check():
    """服务状态检测接口"""
    return success_response(data={
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "jiaxiaohutong-backend",
    })
