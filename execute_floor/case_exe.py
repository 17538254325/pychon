import pytest
import os

pytest.main(["../case_floor/appium_yemian.py","-vs","--alluredir","../report_floor/data"])

os.system("allure generate ../report_floor/data -o ../report_floor/html --clean")