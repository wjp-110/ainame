# ainame

基于 FastAPI + SQLAlchemy(Async) + MySQL 的异步 Web 应用项目，集成邮件发送功能和用户认证系统。

## 📋 项目特性

- **异步框架**: 使用 FastAPI 构建高性能异步 API
- **异步数据库**: SQLAlchemy Async + aiomysql 实现异步数据库操作
- **邮件服务**: 集成 fastapi-mail 支持 SMTP 邮件发送（QQ 邮箱）
- **密码加密**: 使用 pwdlib 进行密码哈希处理
- **分层架构**: Models - Repository - Routers - Schemas 清晰分层
- **数据库迁移**: Alembic 支持数据库版本管理

## 🏗️ 项目结构

 ```
ainame/
├── core/ # 核心功能模块
│ └── mail.py # 邮件服务配置
├── models/ # 数据模型层
│ ├── init.py # 数据库引擎和 Session 配置
│ └── user.py # User 和 EmailCode 模型
├── repository/ # 数据访问层
│ └── user_repo.py # 验证码仓库
├── routers/ # 路由控制器
│ └── auth_router.py # 认证相关路由
├── schemas/ # Pydantic 模式
│ └── init.py # 响应模式定义
├── settings/ # 配置管理
│ └── init.py # 数据库和邮件配置
├── alembic/ # 数据库迁移脚本
├── dependencies.py # FastAPI 依赖注入
├── main.py # 应用入口
└── test_main.http # HTTP 测试文件

```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- MySQL 5.7+ / MariaDB

### 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy aiomysql fastapi-mail pwdlib[argon2] aiosmtplib pydantic email-validator
```

### 配置设置

编辑 `settings/__init__.py` 配置数据库和邮件服务：
```python
数据库配置
DB_URI = "mysql+aiomysql://username:password@host:port/database?charset=utf8mb4"

邮件配置
MAIL_USERNAME="your_email@qq.com"
MAIL_PASSWORD="your_smtp_password"
MAIL_FROM="your_email@qq.com"
MAIL_PORT=587
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="应用名称"
```

### 启动应用

```bash
开发模式启动
uvicorn main:app --reload --host 0.0.0.0 --port 8000
生产环境
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

访问 `http://localhost:8000/docs` 查看 API 文档。

## 📡 API 接口
TODO ....

## 初始化迁移（仅首次)
```bash
alembic init alembic --template init
```
## 创建新迁移
```bash
alembic revision --autogenerate -m "描述信息"
```
## 执行迁移
```bash
alembic upgrade head
```
## 回滚到上一个版本
```bash
alembic downgrade -1
```

