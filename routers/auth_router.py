from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
import string
import random
from fastapi_mail import FastMail, MessageSchema, MessageType
from aiosmtplib import SMTPResponseException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_mail, get_session
from models.user import User
from repository.user_repo import EmailCodeRepository, UserRepository
from core.auth import AuthHandler as auth_handler
from schemas import ResponseOut
from schemas.user import RegisterIn, UserCreateSchema, LoginIn

router = APIRouter(prefix="/auth")

@router.get("/code", response_model=ResponseOut)
async def get_email_code(
        email: Annotated[EmailStr, Query(...)],
        mail: FastMail = Depends(get_mail),
        session: AsyncSession = Depends(get_session),
):
    # 生成验证码
    source = string.digits * 4
    code = "".join(random.sample(source, 4))
    message = MessageSchema(
        subject="注册验证码",
        recipients=[email],
        body=f"您的注册验证码为：{code}，5分钟有效。",
        subtype=MessageType.plain
    )
    try:
        print(f"验证码：{code}")
        await mail.send_message(message)
        email_code_repo = EmailCodeRepository(session)
        await email_code_repo.create(email=str(email), code=code)
    except SMTPResponseException as e:
        # 检查是否是 QQ 特有的二进制响应错误
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("⚠️ 忽略 QQ 邮箱 SMTP 关闭阶段的非标准响应（邮件已成功发送）")
            # 可选：记录日志，但不中断流程
        else:
            raise HTTPException(500, "邮件发送失败！")
    return ResponseOut()

@router.post('/register', response_model=ResponseOut)
async def register(data: RegisterIn, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session)
    if await user_repo.email_is_exist(str(data.email)):
        raise HTTPException(status_code=400, detail="邮箱已经存在！")
    email_code_repo = EmailCodeRepository(session)
    if not await email_code_repo.check_email_code(email=str(data.email), code=data.code):
        raise HTTPException(status_code=400, detail="邮箱验证码错误！")
    await user_repo.create(UserCreateSchema(email=data.email, username=data.username, password=data.password))
    return ResponseOut()

@router.post('/login')
async def login(data: LoginIn, session: AsyncSession = Depends(get_session)):
    # 创建user_repo对象
    user_repo = UserRepository(session)
    # 获取用户
    user: User | None = await user_repo.get_by_email(str(data.email))
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在！")
    if not user.check_password(data.password):
        raise HTTPException(status_code=400, detail="密码错误！")
    # 生成JWToken
    auth_instance = auth_handler()
    tokens = auth_instance.encode_login_token(user.id)
    return {
        "user": user,
        "token": tokens
    }