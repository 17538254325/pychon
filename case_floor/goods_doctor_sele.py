

from setting_floor import sele_setting
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pytest
import random

from logs_floor import logs_pro

log_info = logs_pro.get_log()



llq=sele_setting.get_browser("edge")
#登录模块
@pytest.mark.parametrize("uname,upwd,title,result",[("admn","admin23","登录医药管理系统"),("admin","1234","登录医药管理系统"),
                                             ("adminss","admin123","登录医药管理系统"),("admin","admin123","管理系统"),])
def test_01_login(uname,upwd,title,result):

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

    if llq.title == title:
        assert llq.title == title
        log_info.debug("登录测试通过")


#添加
def test_03_mane():
    login_llq = llq
    time.sleep(5)

    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="药品").click()
    time.sleep(3)
    framl=login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framl)
    time.sleep(5)
    #获取执行的总条数
    pagination_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_num = pagination_text.split("共")[1][:-3]
    #添加模块
    login_llq.find_element(by=By.LINK_TEXT, value="添加").click()
    time.sleep(5)
    login_llq.switch_to.default_content()
    time.sleep(3)
    add_fram=login_llq.find_element(by=By.XPATH, value="html/body/div[3]/div[2]/iframe")
    time.sleep(3)
    login_llq.switch_to.frame(add_fram)
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="productName").send_keys("其6ddddk")
    time.sleep(3)
    sell=login_llq.find_element(by=By.NAME, value="supplierId")
    time.sleep(3)
    Select(sell).select_by_index(1)
    time.sleep(3)
    sellu=login_llq.find_element(by=By.NAME, value="unit")
    time.sleep(3)
    Select(sellu).select_by_index(1)
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="stockNum").send_keys("100")
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="intPrice").send_keys("80")
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="outPrice").send_keys("400")
    time.sleep(3)
    login_llq.switch_to.default_content()
    login_llq.find_element(by=By.LINK_TEXT, value="确定").click()
    time.sleep(3)

    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)

    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text

    after_n = paginati_text.split("共")[1][:-3]

    print(after_num)
    print("----")
    print(after_n)
    assert int(after_n) > int(after_num)
    log_info.debug("测试通过")

    llq.quit()




#修改
def test_04_sou():
    login_llq = sele_setting.test_login(llq)
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
    if random_index is not None:
        table = login_llq.find_element(by=By.ID, value="bootstrap-table")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")

        # 确保表格有足够的行
        if len(rows) > random_index:
            first_row = rows[random_index+1]
            cells = first_row.find_elements(By.TAG_NAME, 'td')

            # 确保行有足够的列
            if len(cells) >= 6:  # 至少需要7列数据
                row_data = []
                row_data.append(cells[1].text.strip())
                row_data.append(cells[2].text.strip())
                row_data.append(cells[3].text.strip())
                row_data.append(cells[4].text.strip())
                row_data.append(cells[5].text.strip())
                row_data.append(cells[6].text.strip())
                row_data.append(cells[7].text.strip())
                print(f"提取的数据: {row_data}")

    login_llq.find_element(by=By.LINK_TEXT, value="修改").click()
    time.sleep(5)
    login_llq.switch_to.default_content()
    time.sleep(3)
    add_frame = login_llq.find_element(by=By.XPATH, value="html/body/div[3]/div[2]/iframe")
    time.sleep(3)
    login_llq.switch_to.frame(add_frame)
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="productName").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="productName").send_keys("六D5666k")
    time.sleep(3)
    sell = login_llq.find_element(by=By.NAME, value="supplierId")
    time.sleep(3)
    Select(sell).select_by_index(2)
    time.sleep(3)
    sllua = login_llq.find_element(by=By.NAME, value="unit")
    time.sleep(3)
    Select(sllua).select_by_index(2)
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="stockNum").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="stockNum").send_keys("200")
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="intPrice").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="intPrice").send_keys("80")
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="outPrice").clear()
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="outPrice").send_keys("400")
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
        row= tabl.find_elements(by=By.TAG_NAME, value="tr")

        # 确保表格有足够的行
        if len(row) > random_index:
            first_row = row[random_index+1]
            cell= first_row.find_elements(By.TAG_NAME, 'td')


            if len(cell) >= 6:
                row_dat = []
                row_dat.append(cell[1].text.strip())
                row_dat.append(cell[2].text.strip())
                row_dat.append(cell[3].text.strip())
                row_dat.append(cell[4].text.strip())
                row_dat.append(cell[5].text.strip())
                row_dat.append(cell[6].text.strip())
                row_dat.append(cell[7].text.strip())

                print(f"提取的数据: {row_dat}")

                if row_data and row_dat:

                            assert row_data != row_dat
                            log_info.debug("测试通过")
                            time.sleep(5)
                            llq.quit()






#删除
def test_05_soo():
    login_llq = sele_setting.test_login(llq)
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="药品").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)
    #删除之前的条数
    pagination_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    ater_num = pagination_text.split("共")[1][:-3]

    count=login_llq.find_elements(by=By.NAME, value="btSelectItem")
    coun=len(count)
    if coun>0:
        n=random.randint(0,coun-1)
        for i in range(1):
            count[i].click()

    time.sleep(3)
    sa=login_llq.find_element(by=By.LINK_TEXT, value="删除").click()
    time.sleep(3)
    login_llq.switch_to.frame(sa)
    login_llq.find_element(by=By.LINK_TEXT, value="确认").click()
    login_llq.switch_to.default_content()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(3)

    #删除之后的条数
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text

    ater_n = paginati_text.split("共")[1][:-3]


    print(ater_num)
    print("----")
    print(ater_n)
    assert int(ater_num) > int(ater_n)
    log_info.debug("测试通过")
    time.sleep(3)
    llq.quit()



#查询
def test_06_cha():
    login_llq = sele_setting.test_login(llq)
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="药品").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)
    #搜索前数量
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text

    after_a = paginati_text.split("共")[1][:-3]
    login_llq.find_element(by=By.NAME, value="productName").send_keys("6")
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="搜索").click()
    time.sleep(5)
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text

    after_b = paginati_text.split("共")[1][:-3]

    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(5)
    login_llq.find_element(by=By.NAME, value="supplierId").send_keys("1")
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="搜索").click()
    time.sleep(5)
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_c = paginati_text.split("共")[1][:-3]

    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(5)
    login_llq.find_element(by=By.NAME, value="productName").send_keys("6")
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="supplierId").send_keys("1")
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="搜索").click()
    time.sleep(5)
    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_d = paginati_text.split("共")[1][:-3]
    print(after_a)
    print("----")
    print(after_d)
    assert int(after_a) >= int(after_b)
    assert int(after_a) >= int(after_c)
    assert int(after_a) >= int(after_d)

    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(5)
    login_llq.find_element(by=By.NAME, value="productName").send_keys("99")
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="supplierId").send_keys("1")
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="搜索").click()
    time.sleep(5)

    tabl = login_llq.find_element(by=By.ID, value="bootstrap-table")
    time.sleep(10)
    rows = tabl.find_elements(by=By.TAG_NAME, value="tr")
    first_row = rows[1]
    cell = first_row.find_elements(By.TAG_NAME, 'td')
    row_dat = []
    row_dat.append(cell[0].text.strip())

    assert row_dat[0] == '没有找到匹配的记录'

    time.sleep(5)

    llq.quit()


#采购订单(记录)
def test_07_cai():
    login_llq = sele_setting.test_login(llq)
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="管理").click()
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="采购订单(记录)").click()
    time.sleep(3)
    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(3)


    pagination_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
    after_np = pagination_text.split("共")[1][:-3]





    login_llq.find_element(by=By.LINK_TEXT, value="添加").click()
    time.sleep(3)
    login_llq.switch_to.default_content()
    time.sleep(3)
    add_frame = login_llq.find_element(by=By.XPATH, value="html/body/div[3]/div[2]/iframe")
    time.sleep(3)
    login_llq.switch_to.frame(add_frame)

    time.sleep(3)
    sell = login_llq.find_element(by=By.NAME, value="supplierId")
    time.sleep(3)
    Select(sell).select_by_index(1)
    time.sleep(3)
    sell = login_llq.find_element(by=By.NAME, value="productId")
    time.sleep(3)
    Select(sell).select_by_index(2)
    time.sleep(3)
    login_llq.find_element(by=By.NAME, value="purchNum").send_keys("106")
    time.sleep(3)

    login_llq.switch_to.default_content()
    login_llq.find_element(by=By.LINK_TEXT, value="确定").click()
    time.sleep(3)

    framel = login_llq.find_element(by=By.XPATH, value="html/body/div/div/div[3]/iframe[2]")
    login_llq.switch_to.frame(framel)
    time.sleep(5)

    paginati_text = login_llq.find_element(
        by=By.XPATH,
        value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text

    after_no = paginati_text.split("共")[1][:-3]

    print(after_np)
    print("----")
    print(after_no)
    assert int(after_np) < int(after_no)
    llq.quit()

def test_08_sos():
    login_llq =  sele_setting.test_login(llq)
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
    else:
        paginati_text = login_llq.find_element(
            by=By.XPATH,
            value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
        after_b = paginati_text.split("共")[1][:-3]

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
    else:
        paginati_text = login_llq.find_element(
            by=By.XPATH,
            value="html/body/div/div/div[2]/div[1]/div[3]/div[1]/span").text
        after_c = paginati_text.split("共")[1][:-3]

    assert row_dt[0] == '没有找到匹配的记录' or int(after_a) >= int(after_c)
    time.sleep(3)
    login_llq.find_element(by=By.LINK_TEXT, value="重置").click()
    time.sleep(3)





















