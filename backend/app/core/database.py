"""异步数据库连接"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """所有模型的基类，自动添加 id / created_at / is_delete"""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # 通用字段由各子类自行声明，此处仅提供软删除查询混入
