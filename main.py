# -*- Coding: utf-8 -*-
# Author: Yu
import pytest
import os

# 运行命令
if __name__ == '__main__':
    # 生成allure相关数据json格式
    pytest.main(["-m", "smoke",
                 "--alluredir=TestResult/report/data_report"])
    # 将allure数据生成测试报告
    os.system("allure generate TestResult/report/data_report -o TestResult/report/allure_report --clean")
    # os.system("allure serve TestResult/report/data_report")
