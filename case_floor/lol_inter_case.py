

from setting_floor import excel_setting,requests_setting
import allure
import pytest

lol_resp_text_list= [];
lol_result_list = [];

@allure.epic("LOL项目接口测试报告")
@allure.feature("lol模块")
@pytest.mark.parametrize("inter_info",excel_setting.read_interface(r"H:\文档\接口测试.xlsx","lol"))
def test_lol_on_inter(inter_info):
    allure.dynamic.title(inter_info.get("shop_name"))
    resp = requests_setting.requests_strong(inter_info.get("shop_requ"), inter_info.get("shop_path"), inter_info.get("shop_query"))

    result_text = requests_setting.if_resp_success(resp, inter_info.get("shop_expected"), inter_info.get("shop_name"))

    lol_resp_text_list.append(resp.text)

    lol_result_list.append(result_text)

def test_write_lol():
    excel_setting.write_test_result(lol_resp_text_list,lol_result_list,r"H:\文档\接口测试.xlsx","lol")





emp_resp_text_list= [];
emp_result_list = [];

@allure.epic("LOL项目接口测试报告")
@allure.feature("emp模块")
@pytest.mark.parametrize("inter_info",excel_setting.read_interface(r"H:\文档\接口测试.xlsx","emp"))
def test_emp_on_inter(inter_info):
    allure.dynamic.title(inter_info.get("shop_name"))
    resp = requests_setting.requests_strong(inter_info.get("shop_requ"), inter_info.get("shop_path"), inter_info.get("shop_query"))

    result_text = requests_setting.if_resp_success(resp, inter_info.get("shop_expected"), inter_info.get("shop_name"))

    emp_resp_text_list.append(resp.text)

    emp_result_list.append(result_text)

def test_write_emp():
    excel_setting.write_test_result(lol_resp_text_list,lol_result_list,r"H:\文档\接口测试.xlsx","emp")



shop_resp_text_list= [];
shop_result_list = [];

@allure.epic("LOL项目接口测试报告")
@allure.feature("shop模块")
@pytest.mark.parametrize("inter_info",excel_setting.read_interface(r"H:\文档\接口测试.xlsx","shop"))
def test_shop_on_inter(inter_info):
    allure.dynamic.title(inter_info.get("shop_name"))
    resp = requests_setting.requests_strong(inter_info.get("shop_requ"), inter_info.get("shop_path"), inter_info.get("shop_query"))

    result_text = requests_setting.if_resp_success(resp, inter_info.get("shop_expected"), inter_info.get("shop_name"))

    shop_resp_text_list.append(resp.text)

    shop_result_list.append(result_text)

def test_write_shop():
    excel_setting.write_test_result(lol_resp_text_list,lol_result_list,r"H:\文档\接口测试.xlsx","shop")
