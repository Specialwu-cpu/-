import jwt
from datetime import datetime, timedelta


# 生成 JWT
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # 设置 token 的有效期
    }
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')  # 使用自定义的密钥进行签名
    return token


# 解码 JWT 并获取用户信息
def decode_token(token):
    try:
        payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        user_id = payload['user_id']
        # 根据 user_id 进行相应的操作，例如从数据库中获取用户信息等
        return user_id
    except jwt.ExpiredSignatureError:
        # token 已过期
        return None
    except jwt.InvalidTokenError:
        # token 无效
        return None
