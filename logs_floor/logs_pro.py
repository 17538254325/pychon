import logging
from datetime import datetime
import os
def get_log():
    # 获取日志对象
    logs_info = logging.getLogger("浏览器自动化测试日志")
    # 设置日志处理级别
    logs_info.setLevel(logging.DEBUG)  # 修改：使用logger对象设置级别

    s_handler = logging.StreamHandler()
    log_file_name = str(datetime.today()).split(" ")[0]
    f_handler = logging.FileHandler("../logs_floor/" + log_file_name + ".log", encoding="utf-8")
    formatter = logging.Formatter("----%(asctime)s---%(name)s---%(levelname)s---%(filename)s:[%(lineno)d]---%(message)s")

    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    logs_info.addHandler(s_handler)
    logs_info.addHandler(f_handler)

    return logs_info







