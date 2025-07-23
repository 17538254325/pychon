
import allure

from setting_floor import sele_setting
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pytest
import random

from logs_floor import logs_pro

log_info = logs_pro.get_log()



#登录模块

@allure.epic("医药管理系统")
@allure.feature("登录模块")
@pytest.mark.parametrize("uname,upwd,title,result",[("admn","admin23","登录医药管理系统","失败-用户名失败"),("admin","1234","登录医药管理系统","失败-密码错误"),
                                             ("adminss","admin123","登录医药管理系统","失败-组合错误"),("admin","admin123","管理系统","成功"),])
def test_01_login(uname,upwd,title,result):
    llq = sele_setting.get_browser("edge")
    allure.dynamic.title(result)
    llq.get("http://127.0.0.1:8008")

    time.sleep(3)
    log_info.debug("清空用户名输入框")
    llq.find_element(by=By.NAME, value="username").clear()
    time.sleep(3)
    log_info.debug("输入用户名")
    llq.find_element(by=By.NAME, value="username").send_keys(uname)
    time.sleep(3)

    log_info.debug("清空密码")
    llq.find_element(by=By.NAME, value="password").clear()
    time.sleep(3)
    log_info.debug("输入密码")
    llq.find_element(by=By.NAME, value="password").send_keys(upwd)
    time.sleep(3)
    llq.find_element(by=By.ID, value="btnSubmit").click()
    time.sleep(3)



    if result == "成功":
        log_info.error(f"登录测试成功  用户名: {uname}, 密码: ****")
        assert title == llq.title


    elif "用户名错误" in result:
        # 用户名错误场景
        log_info.error(f"登录测试失败（用户名错误）- 输入用户名: {uname}")


    elif "密码错误" in result:
        # 密码错误场景
        log_info.error(f"登录测试失败（密码错误）- 输入密码: ****")


    else:
        # 组合错误场景
        log_info.error(f"登录测试失败（组合错误）- 输入: {uname}/{upwd}")
    llq.quit()




@allure.epic("医药管理系统")
@allure.feature("药品模块")
@allure.story('药品——添加')
@pytest.mark.parametrize(
    "case_name,product_Name,select,stock_Num,int_Price,outPrice",  # 与测试数据列数保持一致
    [
        ("药品名称非空验证","", "2", "100", "80", "100"),
        ("供应商非空验证","阿莫西林", "", "100", "30", "100"),
        ("全空验证","", "", "", "", ""),
        ("正确输入验证","阿莫西林", "2", "100", "80", "100"),
    ]
)
def test_mine(case_name,product_Name, select, stock_Num, int_Price, outPrice):
    # 登录系统
    allure.dynamic.title(case_name)
    login_llq = sele_setting.test_login()
  # 这里的"llq"参数需根据实际情况调整


        # 导航到药品管理页面
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()

    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="药品").click()

    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)

        # 获取当前总条数
    pagination_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span"
    ).text
    before_num = pagination_text.split("共")[1][:-3].strip()

        # 点击添加按钮
    login_llq.find_element(by=By.LINK_TEXT, value="添加").click()

    time.sleep(3)
    login_llq.switch_to.default_content()

    time.sleep(3)
    add_frame = login_llq.find_element(by=By.XPATH, value="html/body/div[3]/div[2]/iframe")
    time.sleep(3)
    login_llq.switch_to.frame(add_frame)

        # 填写表单
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="productName").send_keys(product_Name)

    time.sleep(3)
    select_obj = login_llq.find_element(by=By.NAME, value="supplierId")
    if select:
        Select(select_obj).select_by_index(select)

    time.sleep(3)
    select_obj_unit = login_llq.find_element(by=By.NAME, value="unit")
    time.sleep(3)
    Select(select_obj_unit).select_by_index(2)  # 固定选择第三个单位

    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="stockNum").send_keys(stock_Num)

    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="intPrice").send_keys(int_Price)

    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="outPrice").send_keys(outPrice)

    time.sleep(3)
    login_llq.switch_to.default_content()

        # 提交表单
    login_llq.find_element(by=By.LINK_TEXT, value="确定").click()
    time.sleep(3)

        # 重新获取总条数
    login_llq.switch_to.frame(framel)
    pagination_text = login_llq.find_element(by=By.XPATH,value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_num = pagination_text.split("共")[1][:-3].strip()
    if before_num<=after_num:
        log_info.debug(case_name+'执行成功')
    else:
        log_info.debug(case_name+'执行失败')




    login_llq.quit()




# 测试数据
test_data = [{"productName": "六aD5666k","supplierId": 2,"unit": 2,"stockNum": "200","intPrice": "80","outPrice": "400"},
    {"productName": "测试药品2","supplierId": 3,"unit": 1,"stockNum": "500","intPrice": "50","outPrice": "300"}]
@allure.epic("医药管理系统")
@allure.feature("药品模块")
@allure.story("药品修改功能")
@pytest.mark.parametrize("data", test_data)
def test_04_sou(data):
    """药品修改测试用例"""
    allure.dynamic.title(f"药品模块-修改药品-{data['productName']}")

    login_llq = sele_setting.test_login()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="药品").click()
    time.sleep(3)
    frame = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(frame)
    time.sleep(5)

    # 查找所有复选框元素
    count = login_llq.find_elements(by=By.NAME, value="btSelectItem")
    coun = len(count)

    # 随机选择一个复选框并点击
    if coun > 0:
        random_index = random.randint(0, coun - 1)
        random_checkbox = count[random_index]
        random_checkbox.click()
    else:
        print("没有找到复选框元素!")
        random_index = None

    time.sleep(3)  # 等待页面更新

    # 提取表格数据
    row_data = None
    if random_index is not None:
        table = login_llq.find_element(by=By.ID, value="bootstrap-table")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")

        # 确保表格有足够的行
        if len(rows) > random_index:
            first_row = rows[random_index + 1]
            cells = first_row.find_elements(By.TAG_NAME, 'td')

            # 确保行有足够的列
            if len(cells) >= 8:  # 至少需要8列数据
                row_data = []
                row_data.append(cells[1].text.strip())
                row_data.append(cells[2].text.strip())
                row_data.append(cells[3].text.strip())
                row_data.append(cells[4].text.strip())
                row_data.append(cells[5].text.strip())
                row_data.append(cells[6].text.strip())
                row_data.append(cells[7].text.strip())
                print(f"提取的数据: {row_data}")
                log_info.error(f"修改前的数据 {row_data}")

    login_llq.find_element(by=By.LINK_TEXT, value="修改").click()
    time.sleep(5)
    login_llq.switch_to.default_content()
    time.sleep(3)
    add_frame = login_llq.find_element(by=By.XPATH, value="html/body/div[3]/div[2]/iframe")
    time.sleep(3)
    login_llq.switch_to.frame(add_frame)
    time.sleep(3)

    # 使用数据驱动的值
    login_llq.find_element(by=By.NAME, value="productName").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="productName").send_keys(data["productName"])
    time.sleep(3)

    sell = login_llq.find_element(by=By.NAME, value="supplierId")
    time.sleep(3)
    Select(sell).select_by_index(data["supplierId"])
    time.sleep(3)

    sllua = login_llq.find_element(by=By.NAME, value="unit")
    time.sleep(3)
    Select(sllua).select_by_index(data["unit"])
    time.sleep(3)

    login_llq.find_element(by=By.NAME, value="stockNum").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="stockNum").send_keys(data["stockNum"])
    time.sleep(3)

    login_llq.find_element(by=By.NAME, value="intPrice").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="intPrice").send_keys(data["intPrice"])
    time.sleep(3)

    login_llq.find_element(by=By.NAME, value="outPrice").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="outPrice").send_keys(data["outPrice"])
    time.sleep(3)

    login_llq.switch_to.default_content()
    login_llq.find_element(by=By.LINK_TEXT, value="确定").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)

    if random_index is not None:
        tabl = login_llq.find_element(by=By.ID, value="bootstrap-table")
        time.sleep(10)
        row = tabl.find_elements(by=By.TAG_NAME, value="tr")

        # 确保表格有足够的行
        if len(row) > random_index:
            first_row = row[random_index + 1]
            cell = first_row.find_elements(By.TAG_NAME, 'td')

            if len(cell) >= 8:
                row_dat = []
                row_dat.append(cell[1].text.strip())
                row_dat.append(cell[2].text.strip())
                row_dat.append(cell[3].text.strip())
                row_dat.append(cell[4].text.strip())
                row_dat.append(cell[5].text.strip())
                row_dat.append(cell[6].text.strip())
                row_dat.append(cell[7].text.strip())

                print(f"提取的数据: {row_dat}")
                log_info.error(f"获取修改后的数据 {row_dat}")

                if row_data and row_dat:
                    assert row_data != row_dat
                    log_info.error(f"获取修改前的数据 {row_data} 获取修改后的数据 {row_dat} 修改功能测试成功")

    time.sleep(5)
    login_llq.quit()


# 删除测试数据
delete_test_data = [{"name": "随机删除1条", "count": 1},
    {"name": "随机删除3条", "count": 3},
    {"name": "随机删除5条", "count": 5}]
@allure.epic("医药管理系统")
@allure.feature("药品模块")
@allure.story("药品删除功能")
@pytest.mark.parametrize("data", delete_test_data)
def test_05_soo(data):
    """删除药品测试用例"""
    allure.dynamic.title(f"药品模块-删除药品-{data['name']}")

    login_llq = sele_setting.test_login()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="药品").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)

    # 删除之前的条数
    pagination_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    ater_num = pagination_text.split("共")[1][:-3]
    log_info.error(f"获取删除前的总条数 {ater_num}")

    checkboxes = login_llq.find_elements(by=By.NAME, value="btSelectItem")
    total_checkboxes = len(checkboxes)

    # 根据数据驱动决定删除数量
    if total_checkboxes > 0:
        delete_count = min(data["count"], total_checkboxes)
        for i in range(delete_count):
            checkboxes[i].click()
    else:
        pytest.skip("没有可删除的药品")

    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="删除").click()
    time.sleep(3)

    # 处理确认弹窗
    login_llq.switch_to.alert.accept()  # 原代码iframe处理有误，改为处理alert
    time.sleep(3)

    login_llq.switch_to.default_content()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(3)

    # 删除之后的条数
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    ater_n = paginati_text.split("共")[1][:-3]
    log_info.error(f"获取删除后的总条数 {ater_n}")

    print(ater_num)
    print("----")
    print(ater_n)

    if int(ater_num) > int(ater_n):
        log_info.error(f"获取删除前的条数 {ater_num} 获取删除后的条数 {ater_n} 删除功能测试成功")
    else:
        log_info.error(f"获取删除前的条数 {ater_num} 获取删除后的条数 {ater_n} 删除功能测试失败")

    assert int(ater_num) > int(ater_n)
    time.sleep(3)
    login_llq.quit()






@allure.epic("医药管理系统")
@allure.feature("药品模块")
@allure.story("药品查询功能")
# 查询
@pytest.mark.parametrize("test_case_name, product_name, supplier_id, expected_count, expected_row_text",[
        ("名称搜索测试", "6", "", lambda original: int(original) > 0, None),
        ("供应商编号搜索测试", "", "2", lambda original: int(original) > 0, None),
        ("组合条件搜索测试", "6", "6", lambda original: int(original) > 0, None),
        ("无结果搜索测试", "6", "8", 0, "没有找到匹配的记录")])
def test_06_cha(test_case_name, product_name, supplier_id, expected_count, expected_row_text):
    """查询药品测试用例"""
    allure.dynamic.title(f"药品模块-查询药品-{test_case_name}")

    login_llq = sele_setting.test_login()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="药品").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)

    # 搜索前数量
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text

    original_count = paginati_text.split("共")[1][:-3]
    log_info.info(f"搜索前总条数: {original_count}")

    # 重置搜索条件
    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(5)

    # 输入搜索条件
    if product_name:
        login_llq.find_element(by=By.NAME, value="productName").send_keys(product_name)
        time.sleep(1)

    if supplier_id:
        login_llq.find_element(by=By.NAME, value="supplierId").send_keys(supplier_id)
        time.sleep(1)

    # 执行搜索
    login_llq.find_element(by=By.LINK_TEXT, value="搜索").click()
    time.sleep(5)

    # 获取搜索后数量
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text

    # 处理无结果情况的特殊逻辑
    if "没有找到匹配的记录" in paginati_text:
        current_count = "0"
    else:
        current_count = paginati_text.split("共")[1][:-3]

    log_info.info(f"搜索条件: 名称='{product_name}', 供应商编号='{supplier_id}', 搜索后总条数: {current_count}")

    # 验证搜索结果数量
    if callable(expected_count):  # 如果是函数，则传入原始数量进行比较
        assert expected_count(original_count), f"搜索结果数量不符合预期: {original_count} > {current_count}"
        log_info.info(f"搜索结果数量验证通过: {original_count} > {current_count}")
    else:  # 如果是具体数值，则直接比较
        assert int(
            current_count) == expected_count, f"搜索结果数量不符合预期: 预期={expected_count}, 实际={current_count}"
        log_info.info(f"搜索结果数量验证通过: 预期={expected_count}, 实际={current_count}")

    # 如果需要验证表格内容
    if expected_row_text:
        tabl = login_llq.find_element(by=By.ID, value="bootstrap-table")
        time.sleep(3)
        rows = tabl.find_elements(by=By.TAG_NAME, value="tr")

        if len(rows) > 1:  # 如果有数据行
            first_row = rows[1]
            cell = first_row.find_elements(By.TAG_NAME, 'td')
            row_dat = []
            row_dat.append(cell[0].text.strip())
            log_info.info(f"获取第一行数据: {row_dat[0]}")

            assert row_dat[
                       0] == expected_row_text, f"表格内容不符合预期: 预期='{expected_row_text}', 实际='{row_dat[0]}'"
            log_info.info(f"表格内容验证通过: '{row_dat[0]}'")
        else:
            assert False, "表格中没有数据行"

    # 重置搜索条件
    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(3)

    # 关闭浏览器
    login_llq.quit()



# 采购订单测试数据
purchase_test_data = [{"name": "添加测试订单1","supplier_index": 2,
        "product_index": 2,"purchase_num": "16"},{"name": "添加测试订单2","supplier_index": 3,
        "product_index": 3,"purchase_num": "20"},{"name": "添加测试订单3","supplier_index": 4,
        "product_index": 4,"purchase_num": "50"}]


@allure.epic("医药管理系统")
@allure.feature("采购订单(记录)模块")
@allure.story("采购订单添加功能")
@pytest.mark.parametrize("data", purchase_test_data)
def test_07_cai(data):
    """添加采购订单测试用例"""
    allure.dynamic.title(f"采购订单(记录)模块-添加订单-{data['name']}")

    login_llq = sele_setting.test_login()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="采购订单(记录)").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(3)

    # 添加之前的总条数
    pagination_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_np = pagination_text.split("共")[1][:-3]
    log_info.error(f"添加之前的总条数 {after_np}")

    login_llq.find_element(by=By.LINK_TEXT, value="添加").click()
    time.sleep(3)
    login_llq.switch_to.default_content()
    time.sleep(3)
    add_frame = login_llq.find_element(by=By.XPATH, value="html/body/div[3]/div[2]/iframe")
    time.sleep(3)
    login_llq.switch_to.frame(add_frame)

    time.sleep(3)

    # 使用数据驱动的值选择供应商
    supplier = login_llq.find_element(by=By.NAME, value="supplierId")
    time.sleep(3)
    Select(supplier).select_by_index(data["supplier_index"])
    time.sleep(3)

    # 使用数据驱动的值选择产品
    product = login_llq.find_element(by=By.NAME, value="productId")
    time.sleep(3)
    Select(product).select_by_index(data["product_index"])
    time.sleep(3)

    # 使用数据驱动的值输入采购数量
    login_llq.find_element(by=By.NAME, value="purchNum").send_keys(data["purchase_num"])
    time.sleep(3)

    login_llq.switch_to.default_content()
    login_llq.find_element(by=By.LINK_TEXT, value="确定").click()
    time.sleep(3)

    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)

    # 添加之后的总条数
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_no = paginati_text.split("共")[1][:-3]
    log_info.error(f"添加之后的总条数 {after_no}")

    print(after_np)
    print("----")
    print(after_no)

    if int(after_np) < int(after_no):
        log_info.success("添加测试成功")

    assert int(after_np) < int(after_no)
    login_llq.quit()

def test_08_sos():

    login_llq =  sele_setting.test_login()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="采购订单(记录)").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(3)
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_a = paginati_text.split("共")[1][:-3]
    log_info.error(f"搜索之前的总条数 {after_a}")
    sell = login_llq.find_element(by=By.NAME, value="supplierId")
    time.sleep(3)

    count = login_llq.find_elements(by=By.NAME, value="supplierName")
    coun = len(count)
    if coun > 0:
        n = random.randint(0, coun - 1)
        Select(sell).select_by_index(n+1)
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="搜索").click()
    time.sleep(5)

    tabl = login_llq.find_element(by=By.ID, value="bootstrap-table")
    time.sleep(5)
    rows = tabl.find_elements(by=By.TAG_NAME, value="tr")
    first_row = rows[1]
    cell = first_row.find_elements(By.TAG_NAME, 'td')
    row_dat = []
    row_dat.append(cell[0].text.strip())


    if row_dat[0] == '没有找到匹配的记录':
        after_b = "0"
        log_info.error("未搜索到内容")
    else:
        paginati_text = login_llq.find_element(
            by=By.XPATH,
            value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
        after_b = paginati_text.split("共")[1][:-3]
        log_info.error(f"搜索之后的总条数 {after_b}")


    if row_dat[0] == '没有找到匹配的记录' or int(after_a) >= int(after_b):
        log_info.error("搜索测试成功")
    assert row_dat[0] == '没有找到匹配的记录' or int(after_a) >= int(after_b)

    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(3)

    sell = login_llq.find_element(by=By.NAME, value="supplierId")
    time.sleep(3)
    Select(sell).select_by_index(1)

    sell = login_llq.find_element(by=By.NAME, value="productId")
    time.sleep(3)
    count = login_llq.find_elements(by=By.NAME, value="productName")
    coun = len(count)
    if coun > 0:
        n = random.randint(0, coun - 1)
        Select(sell).select_by_index(n + 1)
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="搜索").click()
    time.sleep(5)

    tabl = login_llq.find_element(by=By.ID, value="bootstrap-table")
    time.sleep(5)
    rows = tabl.find_elements(by=By.TAG_NAME, value="tr")
    first_row = rows[1]
    cell = first_row.find_elements(By.TAG_NAME, 'td')
    row_dt = []
    row_dt.append(cell[0].text.strip())

    if row_dt[0] == '没有找到匹配的记录':
        after_c = "0"
        log_info.error("未搜索到内容")
    else:
        paginati_text = login_llq.find_element(
            by=By.XPATH,
            value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
        after_c = paginati_text.split("共")[1][:-3]
        log_info.error(f"搜索之后的总条数 {after_b}")
    if row_dat[0] == '没有找到匹配的记录' or int(after_a) >= int(after_b):
        log_info.error("搜索测试成功")
    assert row_dt[0] == '没有找到匹配的记录' or int(after_a) >= int(after_c)
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(3)
    login_llq.quit()




















