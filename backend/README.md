# 家校互通 - 后端服务 (FastAPI)

> 机构端 + 家长端小程序 / 运营管理 Web 后端

## 开发进度

### ✅ 已完成 (Task 1-3)

| 任务 | 状态 | 内容 |
|------|:----:|------|
| Task 1 | ✅ | FastAPI 骨架：异步 SQLAlchemy+MySQL、JWT 认证(3角色)、CORS、统一响应格式 |
| Task 2 | ✅ | 6 张数据模型(多租户 institution_id 隔离)：platform_admin / institution / org_user / class / student / attendance_record |
| Task 3 | ✅ | 机构注册与审核 API（运营管理端） |

### 🔲 待开发 (Task 4-12)

- [ ] Task 4: 登录认证 API（机构端/家长端登录、获取 token）
- [ ] Task 5: 机构端 - 班级/学员 CRUD
- [ ] Task 6: 考勤打卡接口（手动 + 人脸识别）
- [ ] Task 7: 家长端 API（查看学员考勤）
- [ ] Task 8: 运营管理端 - 数据统计仪表盘
- [ ] Task 9: admin-web (Vue3 前端)
- [ ] Task 10: uni-app 机构端小程序
- [ ] Task 11: uni-app 家长端小程序
- [ ] Task 12: 全链路测试 & 正式部署

---

## 技术栈

- **Python 3.12** + **FastAPI** + **SQLAlchemy 2.0 (async)**
- **MySQL 8.0** (腾讯云数据库)
- **aiomysql** 异步驱动
- **JWT** 认证 (python-jose) + **werkzeug** 密码加密
- **Docker Compose** 一键部署
- **GitHub Actions** CI/CD (PR 合并到 main 自动部署)

## 项目结构

```
backend/
├── app/
│   ├── main.py                  # FastAPI 入口
│   ├── core/                    # 配置、数据库连接、认证、统一响应
│   │   ├── config.py            # 环境变量配置 (pydantic-settings)
│   │   ├── database.py          # 异步引擎 + Session
│   │   ├── auth.py              # JWT 签发/验证 + 角色守卫
│   │   └── response.py          # {code, msg, data} 统一格式
│   ├── models/                  # SQLAlchemy ORM 模型
│   │   ├── base.py              # TimestampMixin (id/created_at/is_delete)
│   │   ├── platform_admin.py    # 平台管理员
│   │   ├── institution.py       # 机构（租户主体）
│   │   ├── org_user.py          # 机构用户(principal/teacher)
│   │   ├── class_model.py       # 班级
│   │   ├── student.py           # 学员（含人脸URL预留）
│   │   └── attendance_record.py # 考勤记录
│   ├── schemas/                 # Pydantic 请求/响应模型
│   │   └── institution.py       # 注册/审核相关 Schema
│   ├── services/                # 业务逻辑层
│   │   └── institution_service.py
│   └── api/                     # 路由层
│       ├── health.py            # GET /api/health
│       └── institution.py       # 机构注册与审核 (3个接口)
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
└── .github/workflows/deploy.yml
```

## 已有 API 接口

| 方法 | 路径 | 认证 | 说明 |
|------|------|:----:|------|
| `GET` | `/api/health` | 无 | 服务健康检查 |
| `POST` | `/api/platform/institutions/` | 无 | 机构注册申请 |
| `GET` | `/api/platform/institutions/` | platform_admin | 机构列表（分页+筛选） |
| `PUT` | `/api/platform/institutions/{id}/review` | platform_admin | 审批机构（通过自动创建校长账号） |

## 快速启动

```bash
# 1. 复制环境变量并编辑
cp .env.example .env
# 编辑 .env，填入 MySQL 连接信息等

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python -m app.main
# 或使用 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

访问 `http://localhost:8000/docs` 查看 Swagger 文档。

## 部署

```bash
# Docker Compose 部署
cp .env.example .env   # 填入生产环境配置
docker compose up -d --build
```

GitHub Actions: 向 `main` 分支提交 PR 并合并后，自动部署至腾讯云服务器。
