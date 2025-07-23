from appium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# 用户登录信息
USERNAME = "17538254325"
PASSWORD = "123456"


def login_to_lightnote(username=USERNAME, password=PASSWORD):
    print("准备启动Appium驱动...")

    # 配置Appium驱动
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "9",
        "deviceName": "emulator-5554",
        "appPackage": "com.luyun.lightnote",
        "appActivity": "com.luyun.lightnote.ui.SplashActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "noReset": False,
        "newCommandTimeout": 600,
        "automationName": "UIAutomator2"
    }

    # 连接到Appium服务器并启动应用
    print("正在连接Appium服务器...")
    time.sleep(2)
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
    print("✅ 应用已成功启动")

    # 处理用户协议弹窗
    print("检查用户协议弹窗...")
    agree_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/md_buttonDefaultPositive"))
    )
    agree_button.click()
    print("✅ 已同意用户协议")
    time.sleep(2)

    # 处理启动广告（修改部分：明确判断广告是否存在）
    print("检查启动广告...")
    time.sleep(4)
    # 先查找"跳过"按钮，设置较短的超时时间
    ad_elements = driver.find_elements(By.XPATH, "//*[contains(@text, '跳过')]")

    # 如果找到广告元素，则点击；否则继续执行
    if len(ad_elements) > 0:
        ad_elements[0].click()
        print("✅ 已跳过广告")
    else:
        print("ℹ️ 未找到启动广告，继续执行")

    # 点击登录按钮
    print("寻找登录按钮...")
    login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/btn_login"))
    )
    login_button.click()
    print("✅ 已进入登录页面")

    # 输入手机号
    print("输入手机号...")
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/et_mobile_email"))
    )
    phone_input.clear()
    phone_input.send_keys(username)
    print(f"✅ 已输入手机号: {username}")

    # 输入密码
    print("输入密码...")
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/et_psd"))
    )
    password_input.clear()
    password_input.send_keys(password)
    print("✅ 已输入密码")

    # 勾选用户协议
    print("检查用户协议勾选框...")
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/cb_agreement"))
    )
    if not checkbox.is_selected():
        checkbox.click()
        print("✅ 已勾选用户协议")
    else:
        print("ℹ️ 用户协议已勾选")

    # 提交登录
    print("提交登录请求...")
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "com.luyun.lightnote:id/btn_login"))
    )
    submit_button.click()
    print("✅ 已提交登录请求")

    # 处理登录后弹窗（修改部分：使用find_elements避免异常）
    print("检查登录后弹窗...")
    popup_buttons = driver.find_elements(By.XPATH, "//*[contains(@text, '取消')]")
    if len(popup_buttons) > 0:
        popup_buttons[0].click()
        print("✅ 已关闭登录后弹窗")
    else:
        print("ℹ️ 未找到登录后弹窗，继续执行")

    # 验证登录成功
    print("验证登录是否成功...")

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "com.luyun.lightnote:id/tv_title"))
    )
    print("✅ 登录成功，已进入首页")

    return driver


# 测试主函数
if __name__ == "__main__":
    print("开始执行登录测试...")
    driver = login_to_lightnote()
