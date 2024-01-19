#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File    ：__init__.py
@Author  ：zhubin_n@outlook.com
@Date    ：2023/5/19 20:21 
'''
from openfinance.datacenter.database.quant.engine.calc import *
from openfinance.datacenter.database.quant.engine.base import QuantManager


QuantManager().register(
    "macd", macd
)

QuantManager().register(
    "ma", ma
)