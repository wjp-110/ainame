from datetime import timedelta


DB_URI = "mysql+aiomysql://root:123456@127.0.0.1:3306/ainame?charset=utf8mb4"

# 邮箱相关配置
MAIL_USERNAME="xxxxxx@qq.com"
MAIL_PASSWORD="xxxxxxxxxxxxxx"
MAIL_FROM="xxxxxx@qq.com"
MAIL_PORT=587
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="测试ainame"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False

JWT_SECRET_KEY = "sdad3ddasdada"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
