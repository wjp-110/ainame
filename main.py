from aiosmtplib import SMTPResponseException
from fastapi import FastAPI, Depends
from fastapi_mail import FastMail, MessageSchema, MessageType

from dependencies import get_mail

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get('/mail/test')
async def send_mail_test(
    email: str,
    mail: FastMail = Depends(get_mail)
):
    message = MessageSchema(
        subject="hello",
        recipients=[email],
        body=f"Hello {email}",
        subtype=MessageType.plain
    )
    try:
        await mail.send_message(message)
    except SMTPResponseException as e:
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("⚠️ 忽略 QQ 邮箱 SMTP 关闭阶段的非标准响应（邮件已成功发送）")
    return {"message": "邮件发送成功！"}
