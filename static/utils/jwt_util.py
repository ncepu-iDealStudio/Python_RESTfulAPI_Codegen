# !/user/bin/env python
# coding=utf-8

"""
token生成与解密工具
"""
import time
from datetime import datetime, timedelta
from authlib.jose import jwt, JoseError


class JwtToken(object):
    _expire_message = dict(code=1200, msg="token 已经失效")

    _unknown_error_message = dict(code=4200, msg="token 解析失败")

    # 生成token
    @classmethod
    def generate_token(cls, data: dict, secret_key: str, expires_in: int = 3600) -> str:

        # 签名算法
        header = {'alg': 'HS256'}
        # 用于签名的密钥
        key = secret_key
        # 待签名的数据负载
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        payload.update(data)
        print(payload)

        token = jwt.encode(header=header, payload=payload, key=key).decode("ascii")

        return token

    # token解析
    # token解析通过则返回(True, data),否则返回(False, err)
    @classmethod
    def parse_token(cls, token: str, secret_key: str) -> tuple:
        payload_data = {}
        verify_status = False
        try:
            payload_data = jwt.decode(token, secret_key)
            # print(payload_data)

            expiration_time = payload_data.get('exp', None)
            # 验证token是否过期
            if expiration_time:
                # 获取当前时间戳
                current_time = int(time.time())
                # 检查 token 是否过期
                if current_time <= expiration_time:
                    verify_status = True
                else:
                    payload_data['err'] = "token 已经失效"

        except Exception as _err:
            payload_data["err"] = "token 解析失败"

        return verify_status, payload_data
