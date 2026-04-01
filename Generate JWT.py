import jwt
import datetime

def generate_jwt(user_id, secret_key):
    """
    生成JWT令牌
    
    Args:
        user_id: 用户ID
        secret_key: 密钥
    
    Returns:
        str: JWT令牌
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token




def verify_jwt(token, secret_key):
    """
    验证JWT令牌
    
    Args:
        token: JWT令牌
        secret_key: 密钥
    
    Returns:
        dict: 解码后的payload，如果无效返回None
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token已过期")
        return None
    except jwt.InvalidTokenError:
        print("无效的Token")
        return None





if __name__ == "__main__":
    secret = "your-secret-key-here"
    user_id = 123
    
    token = generate_jwt(user_id, secret)
    print(f"生成的JWT: {token}")
    
    decoded = verify_jwt(token, secret)
    if decoded:
        print(f"解码成功: {decoded}")