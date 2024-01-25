#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:token.py
# author:JackieX
# datetime:2024-01-25 18:40
# software: PyCharm

"""
 生成和校验token的工具类
"""


from authlib.jose import jwt, JoseError
from datetime import datetime, timedelta, timezone


class TokenService:
    def __init__(self, secret_key, algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_token(self, expires, **kwargs):
        now = datetime.now(timezone.utc)
        exp = now + timedelta(seconds=expires)
        payload = {
            'exp': exp,
            **kwargs
        }
        return jwt.encode(header={'alg': self.algorithm}, payload=payload, key=self.secret_key, check=True)

    def verify_token(self, token):
        try:
            return jwt.decode(token, key=self.secret_key)

        except JoseError as e:
            return str(e)

    def get_userinfo_by_token(self, token):
        payload = self.verify_token(token)
        if isinstance(payload, dict):
            return payload.get('user_info', payload)
        return payload


if __name__ == '__main__':
    secret_key = 'your_secret_key'
    kwargs = {'username': 'kevin', 'role': 'admin'}
    expires_in = 3600

    token_service = TokenService(secret_key)
    res = token_service.generate_token(expires_in, **kwargs)

    print("token:", res)

    user_info = token_service.get_userinfo_by_token(res)
    print('User Info:', user_info)