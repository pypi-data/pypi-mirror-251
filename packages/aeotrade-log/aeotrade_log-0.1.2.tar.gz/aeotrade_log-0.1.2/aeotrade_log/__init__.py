"""
@company: 慧贸天下(北京)科技有限公司
@author: wanghao@aeotrade.com
@time: 2024/1/19 9:49 
@file: __init__.py
@project: aeotrade_log
@describe: None
"""
from .handlers import MonthlyRotatingFileHandler, MyLogFormatter

###################################################################
# aeotrade_log是实现了符合慧贸天下(北京)科技有限公司日志配置规范的日志模块   #
# 由慧贸天下(北京)科技有限公司Python组维护                              #
#                                                                 #
# 最近更新人: wanghao@aeotrade.com                                  #
# 最近更新时间:2024/1/19                                            #
###################################################################


__all__ = [
    "MonthlyRotatingFileHandler",
    "MyLogFormatter",
]

# Make nicer public names.
__locals = locals()
for __name in __all__:
    if not __name.startswith(("__", "DEFAULT_")) and not __name.islower():
        __locals[__name].__module__ = "aeotrade_log"
del __locals
del __name  # pyright: ignore[reportUnboundVariable]
