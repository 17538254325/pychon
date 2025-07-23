


import requests
import json
import difflib
from logs_floor import logs_pro


log_info = logs_pro.get_log();

def requests_strong(inter_method,inter_url,inter_parms):
    inter_method=inter_method.lower()

    if inter_method == "get" or inter_method=="delete":
        result = requests.get(url=inter_url,params=json.loads(inter_parms))

    elif inter_method == "post" or inter_method=="update":

        result = requests.post(url=inter_url,data=json.loads(inter_parms))

    return result

def if_resp_success(result,inter_think,intername):

    if result.status_code == 200 and difflib.SequenceMatcher(None,inter_think,result.text).ratio()>0.6:
        log_info.debug(intername+"接口测试通过")
        return "√"

    else:
        log_info.info(intername+"接口测试不通过")
        return "x"