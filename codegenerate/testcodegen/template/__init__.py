#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    日志初始化
"""

import loguru

loguru.logger.add(
    'logs/test_log.log',
    rotation="2 MB",
    encoding="utf-8",
)
