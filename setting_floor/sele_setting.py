from selenium import webdriver
import time
from selenium.webdriver.common.by import By




def get_browser(browse_name):
    if browse_name == "chrome":
       return webdriver.Chrome();
    elif browse_name == "firefox":
        return webdriver.Firefox();
    elif browse_name == ("edge"):
        return webdriver.Edge();
    else:
        print("你调用的浏览器暂不支持！")
def test_login():
    llq = get_browser("edge")
    llq.get("http://127.0.0.1:8008/")
    time.sleep(3)

    llq.find_element(by=By.NAME, value="username").clear()
    time.sleep(1)
    llq.find_element(by=By.NAME, value="username").send_keys("admin")
    time.sleep(1)

    llq.find_element(by=By.NAME, value="password").clear()
    time.sleep(1)
    llq.find_element(by=By.NAME, value="password").send_keys("admin123")
    time.sleep(1)
    llq.find_element(by=By.ID, value="btnSubmit").click()
    time.sleep(5)

    return llq



