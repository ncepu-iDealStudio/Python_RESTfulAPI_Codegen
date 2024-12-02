#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@file: __init__.py.py
@time: 2023/4/16 22:35

"""
"""
    日志初始化
"""

from loguru import logger

logger.add(
    'logs/test_log-{time:YYYY-MM-DD}.log',
    rotation="2 MB",
    encoding="utf-8",
)
