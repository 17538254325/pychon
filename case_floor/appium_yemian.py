from setting_floor.appium_moni import login_to_lightnote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import allure

import pytest


from logs_floor import logs_pro


log_info = logs_pro.get_log()



TEST_CASES = [{"new_title": "测试标题1", "new_content": "测试内容1", "case_name": "基础修改"},
    {"new_title": "标题2", "new_content": "内容2", "case_name": "第二次修改"},]

@allure.epic("轻记事本")
@allure.story("记事修改功能")
@pytest.mark.parametrize("data", TEST_CASES)
def test_01_ote():

    print("===== 开始测试编辑笔记 =====")

    # 1. 登录并进入首页
    driver = login_to_lightnote()
    assert driver, "❌ 登录失败，测试终止"
    log_info.debug("登录成功")

    # 确认在首页
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/tv_title"))
    )
    print("✅ 已在首页（笔记列表页）")

    # 2. 循环执行测试用例
    for i, case in enumerate(TEST_CASES):
        print(f"\n===== 执行用例 {i + 1}/{len(TEST_CASES)}: {case['case_name']} =====")

        # 步骤2：点击菜单→编辑按钮
        print("点击菜单按钮...")
        menu_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/iv_action"))
        )
        menu_btn.click()

        print("点击编辑按钮...")
        edit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@text='编辑']"))
        )
        edit_btn.click()
        print("✅ 进入编辑模式")
        time.sleep(1)  # 等待页面加载

        # 步骤3：输入新的标题和内容
        print("修改标题...")
        title_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/et_title"))
        )
        title_input.clear()
        title_input.send_keys(case['new_title'])

        # 编辑内容（坐标点击）
        print(f"修改内容为: {case['new_content']}")
        content_center_x = (32 + 868) // 2
        content_center_y = (260 + 1584) // 2

        # 点击内容区域
        driver.tap([(content_center_x, content_center_y)], 500)
        time.sleep(2)

        # 检查焦点元素（无异常处理）
        focused_elem = driver.find_element(By.XPATH, '//*[@focused="true"]')
        print(f"当前焦点元素：{focused_elem.get_attribute('resourceId')}")

        # 验证是否命中内容输入框
        if "et_content" not in focused_elem.get_attribute('resourceId'):
            print("❌ 点击未命中输入框，调整坐标")
            driver.tap([(content_center_x, content_center_y - 50)], 500)
        print("✅ 标题和内容修改完成")

        # 步骤4：点击保存按钮
        print("点击保存按钮...")
        save_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/menu_save"))
        )
        save_btn.click()
        print("✅ 已保存，等待返回首页...")
        log_info.debug('已保存')

        # 步骤5：验证回到首页
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/tv_title"))
        )
        print("✅ 已返回首页，准备下一个用例")

    print("\n===== 所有测试用例执行完毕 =====")
    driver.quit()
    print("✅ 测试结束，关闭应用")
    log_info.debug('编辑测试完毕')







@allure.epic("轻记事本")
@allure.feature("搜索")
def test_02_search():
    allure.dynamic.title("搜索")
    driver = login_to_lightnote()
    print("登录成功，开始搜索测试")
    log_info.debug('开始搜索测试')

    # 步骤1：点击搜索按钮（无显式等待，用固定延迟）
    time.sleep(3)  # 等待页面加载
    search_btn = driver.find_element(By.ID, "com.luyun.lightnote:id/id_search_btn")
    search_btn.click()
    print("已点击搜索按钮")
    time.sleep(2)  # 等待搜索界面打开

    # 步骤2：输入关键词（无显式等待）
    search_input = driver.find_element(By.ID, "com.luyun.lightnote:id/et_search")
    search_input.clear()
    time.sleep(1)  # 等待输入框就绪
    search_input.send_keys("欢迎")
    actual_text = search_input.get_attribute('text')
    print(f"实际输入内容：{actual_text}")
    os.system('adb shell input keyevent 66')
    log_info.debug("已通过纯 adb 触发搜索")
    time.sleep(3)







@allure.epic("轻记事本")
@allure.feature("新增")
def test_03_saaarch():
    allure.dynamic.title("新增")
    TARGET_DATA = "测试"
    driver = login_to_lightnote()
    print("登录成功，开始新增测试")
    time.sleep(4)  # 等待页面加载
    # 替换原有定位代码
    note_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.widget.RelativeLayout"))
    )
    note_btn.click()
    print("点击底部记事按钮，触发新建记事")
    time.sleep(3)

    search_btn = driver.find_element(By.ID, "com.luyun.lightnote:id/icon")
    search_btn.click()
    print("笔记")
    time.sleep(3)
    title_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/et_title")))
    title_input.clear()
    title_input.send_keys(TARGET_DATA)
    #标题
    title_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/et_content")))
    title_input.clear()
    title_input.send_keys("测试分为几个板块")
    time.sleep(2)
    search_btn = driver.find_element(By.ID, "com.luyun.lightnote:id/menu_save")
    search_btn.click()
    time.sleep(2)
    recycler_view = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "com.luyun.lightnote:id/rcv_note")))
    items = recycler_view.find_elements(By.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView$ViewHolder")

    data_found = False
    for item in items:
        item_text = item.text
        if TARGET_DATA in item_text:
            data_found = True
            print(f"找到新增笔记：{item_text}")
            break

    # 断言验证结果
    assert data_found, f"未找到标题包含「{TARGET_DATA}」的笔记"
    log_info.debug(f"✅ 笔记「{TARGET_DATA}」已成功添加并显示")




@allure.epic("轻记事本")
@allure.feature("新增")
def test_04_shoucang():
    allure.dynamic.title("收藏")
    driver = login_to_lightnote()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/tv_title"))
    )
    print("✅ 已在首页（笔记列表页）")
    print("点击菜单按钮...")
    menu_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/iv_action"))
    )
    menu_btn.click()

    print("点击收藏按钮...")
    edit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@text='收藏']"))
    )
    edit_btn.click()
    log_info.debug("已收藏")
    time.sleep(1)




@allure.epic("轻记事本")
@allure.feature("帅选")
def test_05_shaixuan():
    allure.dynamic.title("筛选")
    driver = login_to_lightnote()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/tv_title"))
    )
    log_info.debug("✅ 已在首页（笔记列表页）")
    time.sleep(2)
    log_info.debug("点击菜单按钮...")
    menu_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_btn.click()
    time.sleep(4)
    ave_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_note")))
    textt = ave_btn.text
    ave_btn.click()
    time.sleep(4)
    save_bt= WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    text=save_bt.text
    assert text == textt
    log_info.debug("笔记测试成功")

    menu_bn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_bn.click()
    time.sleep(4)
    save_aa_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_draw")))
    xinxa = save_aa_btn.text
    save_aa_btn.click()
    time.sleep(4)
    sve_btnaa = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    xina = sve_btnaa.text
    assert xina == xinxa
    log_info.debug("绘画测试成功")


    menu_bn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_bn.click()
    time.sleep(4)
    save_batn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_mood")))
    xinxaa= save_batn.text
    save_batn.click()
    time.sleep(4)
    svea_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    xinaa = svea_btn.text
    assert xinaa == xinxaa
    log_info.debug("绘画测试成功")

    menu_bn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_bn.click()
    time.sleep(4)
    saveaa_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_todo")))
    xinxee = saveaa_btn.text
    saveaa_btn.click()
    time.sleep(4)
    sveee_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    xinee = sveee_btn.text
    assert xinee == xinxee
    log_info.debug("清单测试成功")

    menu_bn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_bn.click()
    time.sleep(4)
    aasave_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_link")))
    xinxll = aasave_btn.text
    aasave_btn.click()
    time.sleep(4)
    sve_btnll = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    xinll = sve_btnll.text
    assert xinll == xinxll
    log_info.debug("链接测试成功")

    menu_bn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_bn.click()
    time.sleep(4)
    save_btnoo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_bank_card")))
    xinxii = save_btnoo.text
    save_btnoo.click()
    time.sleep(4)
    sve_btnii = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    xinii= sve_btnii.text
    assert xinii == xinxii
    log_info.debug("银行卡测试成功")


    menu_bn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_bn.click()
    time.sleep(4)
    save_btppn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_account")))
    xinxpp = save_btppn.text
    save_btppn.click()
    time.sleep(4)
    sve_btnpp = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    xinpp = sve_btnpp.text
    assert xinpp == xinxpp
    log_info.debug("账户测试成功")

    menu_bn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/id_drawer_btn")))
    menu_bn.click()
    time.sleep(4)
    save_btnuu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/rl_mind")))
    xinxuu = save_btnuu.text
    save_btnuu.click()
    time.sleep(4)
    svuue_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "android.view.View")))
    xinuu = svuue_btn.text
    assert xinuu == xinxuu
    log_info.debug("思维导图测试成功")






def test_06_shanchu():
    driver = login_to_lightnote()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/tv_title")))
    log_info.debug("✅ 已在首页（笔记列表页）")
    time.sleep(2)
    save_btnuu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/iv_action")))
    save_btnuu.click()
    edit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@text='删除']")))
    edit_btn.click()
    time.sleep(2)
    save_btanuu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/md_buttonDefaultPositive")))
    save_btanuu.click()
    log_info.debug("删除成功")






