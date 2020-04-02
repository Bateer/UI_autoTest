# -*- Coding: utf-8 -*-
# Author: Yu
# todo: 存放其他文件所需配置路径
# 主要是用于获取存放日志、测试用例、测试数据、测试结果等路径配置文件

import os

# 最顶层目录到/UI_autoTest，方便后面调用路径配置
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取测试用例的路径
testCase_path = os.path.join(base_dir, "TestCase")

# 获取测试数据的路径
testData_path = os.path.join(base_dir, "TestData")

# 获取测试报告的路径
testResult_path = os.path.join(base_dir, "TestResult")

# 获取日志的路径
logs_path = os.path.join(base_dir, "TestResult\logs")

# 获取截图的路径
picture_path = os.path.join(base_dir, "TestResult\Picture")
