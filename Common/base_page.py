# -*- Coding: utf-8 -*-
# Author: Yu
# todo: 重构find等方法
# 主要是通过重构find等方法，方便后面直接调用，并且加上日志

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webdriver import WebDriver
from Common.globalLogger import globale_logInfo
from selenium.webdriver.common.by import By
from Common import dir_path
from time import sleep
import time
import datetime
import traceback


# 对页面上的异常弹窗等进行异常处理的装饰器
def exception_handle(func):
    def wrapper(*args, **kwargs):
        # 调用下面的类
        _self: BasePage = args[0]
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # 超过异常处理次数直接抛异常
            if _self._error_count > _self._error_max:
                raise e
            _self._error_count += 1
            # 循环黑名单里面的元素，挨个匹配是否能够在页面上找到，找到就点击掉
            for element in _self._back_list:
                new_element = (element[0], element[2])
                elemets = _self._driver.find_elements(*new_element)
                if len(elemets) > 0:
                    elemets[0].click()
                return wrapper(*args, *kwargs)
            raise e

    return wrapper


class BasePage(object):
    _base_url = ''
    _driver = None
    _logger = globale_logInfo()
    # 异常处理的黑名单
    _back_list = [
        (By.ID, "首页", "tv_agree"),
        (By.ID, "开户", "image_cancel")
    ]
    # 异常处理的次数
    _error_max = 5
    _error_count = 0

    # 定义默认会启动chrome的webdriver
    def __init__(self, driver: WebDriver = None, reuse=False):
        if driver is None:
            if reuse:
                option = webdriver.ChromeOptions()
                # 使用已经存在的chrome进程
                option.debugger_address = None  #
                self._driver = webdriver.Chrome(options=option)
            else:
                # index页面用这个方法
                self._driver = webdriver.Chrome()
            self._driver.implicitly_wait(3)
        else:
            # 如果driver是存在的
            # Login与Register等页面需要用这个方法
            self._driver = driver

        try:
            if self._base_url != '':  # 判断请求连接是否为空
                self._driver.get(self._base_url)
        except Exception as e:
            self._logger.error("该请求url为空")

    # 重新定义find方法
    @exception_handle  # 加上异常处理装饰器
    def find(self, by, locator="", page_name = ''):
        """

        :param by: By.Path等，定位元素的方法
        :param locator:  定位元素
        :return:  返回为定位元素值
        """
        try:
            # 判断是否为元组形式传入
            if isinstance(by, tuple):
                self._logger.info("page_name:{0}---{1}元素找到".format(page_name, *by))
                return self._driver.find_element(*by)
            else:
                self._logger.info("page_name:{0}---{1}元素找到".format(page_name, locator))
                return self._driver.find_element(by, locator)
        except Exception as e:
            self._logger.error("page_name:{0}---元素查找失败".format(page_name))
            self.save_screeshot(page_name)

    # 截图保存函数
    def save_screeshot(self, page_name):
        """

        :param page_name:  当前页面的名字
        :return:
        """
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())  # 记录当前时间
        screenshot_path = dir_path.picture_path + "/{}_{}.jpg".format(page_name, now)  # 图片存放路径格式
        try:
            self._driver.save_screenshot(screenshot_path)
        except:
            self._logger.exception("当前页面{0}截图保存失败".format(page_name))
        else:
            self._logger.info("保存{0}截图成功".format(page_name))

# 隐式等待元素可见函数
    def wait_invisibility_element(self, locator, page_name, timeout=30, poll_frequency=0.5):
        """

        :param loctor: 定位元素位置
        :param page_name: 当前页面名字，方便记录日志
        :param timeout: 页面等待超时时间
        :param poll_frequency: 检测的间隔步长，默认为0.5s
        :return:
        """
        self._logger.info("pageName:{0}---等待该元素{1}可见".format(page_name, locator))
        try:
            # 记录下元素加载开始时间
            start_time = datetime.datetime.now()
            # 隐式等待加载元素可见
            WebDriverWait(self._driver, timeout, poll_frequency)\
                .until(expected_conditions.invisibility_of_element_located(locator))
        except Exception as e:
            # 记录下异常，如果元素加载超时或者失败
            self._logger.error("pageName:{0}-----{1}元素加载失败：{2}".format(page_name, locator, e))
            self.save_screeshot(page_name)
            raise
        else:
            # 记录下元素加载最后结束时间
            end_time = datetime.datetime.now()
            load_time = end_time-start_time
            self._logger.info("pageName:{0}----{1}元素加载完成，一共花费时间{2}".format(
                page_name,
                locator,
                load_time
            ))

# 隐式等待元素存在
    def wait_contains_element(self, locator, page_name, timeout=30, poll_fre=0.5):
        self._logger.info("pageName:{0}---等待{1}元素存在".format(page_name, locator))
        try:
            # 起始等待的时间 datetime
            start_time = datetime.datetime.now()
            WebDriverWait(self._driver, timeout, poll_fre).\
                until(expected_conditions.presence_of_element_located(locator))
        except:
            # 异常信息写入日志
            self._logger.error("等待元素存在失败：")
            self.save_screeshot(page_name)
            raise
        else:
            # 结束等待的时间
            end_time = datetime.datetime.now()
            load_time = end_time - start_time
            self._logger.info("pageName:{0}---{1}元素可点击加载完成，一共花费{2}".format(
                page_name,
                locator,
                load_time
            ))

# 隐式等待元素可点击
    def wait_click_element(self, locator, page_name, timeout=30, poll_frequency=0.5):
        """

        :param locator: 定位到的元素
        :param timeout: 等待元素时间，设置超时时间，单位S
        :param poll_frequency: 检测的间隔步长，默认为0.5s
        :return:
        """
        # 记录元素日志
        self._logger.info("pageName:{0}---等待{1}元素可点击".format(
            page_name,
            locator
        ))
        # 处理隐式等待元素可点击
        try:
            # 记录下元素加载时间
            start_time = datetime.datetime.now()
            WebDriverWait(self._driver, timeout, poll_frequency).\
                until(expected_conditions.element_to_be_clickable(locator))
        except Exception as e:
            # 加载元素失败或者超时
            self._logger.error("pageName:{0}---该元素{1}加载失败，原因:{2}".format(
                page_name,
                locator,
                e
            ))
            self.save_screeshot(page_name)
            raise
        else:
            # 记录下加载时间
            end_time = datetime.datetime.now()
            load_time = end_time - start_time
            self._logger.info("pageName:{0}---{1}元素可点击加载完成，一共花费{2}".format(
                page_name,
                locator,
                load_time
            ))

# 隐式等待元素定位并且可被选择
    def wait_selected_element(self, locator, page_name, timeout=30, poll_frequency=0.5):
        """

        :param locator: 元素定位的位置
        :param page_name: 当前页面名称
        :param timeout: 超时时间
        :param poll_frequency: 检测的间隔步长，默认为0.5s
        :return:
        """
        # 在日志中记录下元素
        self._logger.info("pageName:{0}---等待{1}元素加载被选中".format(
            page_name,
            locator
        ))
        try:
            start_time = datetime.datetime.now()  # 计算元素加载开始时间
            WebDriverWait(self._driver, timeout, poll_frequency).\
                until(expected_conditions.element_located_to_be_selected(locator))  # 元素加载定位到并且被选中
        except Exception as e:
            # 元素加载失败或者加载超时
            self._logger.error("pageName:{0}---该元素{1}加载失败，原因:{2}".format(
                page_name,
                locator,
                e
            ))
            self.save_screeshot(page_name)
            raise
        else:
            # 记录下加载时间
            end_time = datetime.datetime.now()
            load_time = end_time-start_time
            self._logger.info("pageName:{0}---{1}元素可点击加载完成，一共花费{2}".format(
                page_name,
                locator,
                load_time
            ))

# 输入文本信息
    def input_keys(self, locator_name, value, page_name, timeout=30, poll_frequency=0.5):
        """

        :param locator: 定位的元素
        :param value: 输入文本的值
        :param page_name: 页面名字
        :param timeout: 元素加载超时时间，单位S
        :param poll_frequency: 检测的间隔步长，默认为0.5s
        :return:
        """
        # 1. 先隐式等待元素可见；
        # 2. 定位到该元素，输入文本操作
        self.wait_invisibility_element(locator_name, page_name, timeout, poll_frequency)
        ele = self.find(locator_name, page_name)
        self._logger.info("pageName:{0}---对{1}元素输入文本：{2}".format(
            page_name,
            locator_name,
            value
        ))
        try:
            ele.send_keys(value)
        except Exception as e:
            # 输入文本失败，记录日志中
            self._logger.error("pageName:{0}---对{1}元素输入文本失败，原因:{2}".format(
                page_name,
                locator_name,
                e
            ))
            self.save_screeshot(page_name)
            raise

# 点击该元素
    def element_click(self, locator_name, page_name, timeout=30, poll_frequency=0.5):
        # 1. 先隐式等待元素可见；
        # 2. 定位到该元素，点击元素操作
        self.wait_invisibility_element(locator_name, page_name, timeout=30, poll_frequency=0.5)
        ele = self.find(locator_name, page_name)
        self._logger.info("pageName:{0}---对{1}元素进行点击".format(
            page_name,
            locator_name
        ))
        try:
            ele.click()
        except Exception as e:
            # 点击元素失败,日志记录，然保存截图
            self._logger.error("pageName:{0}---对{1}元素点击失败，原因：{2}".format(
                page_name,
                locator_name,
                e
            ))
            self.save_screeshot(page_name)

# 获取元素文本值
    def get_element_text(self, locator_name, page_name, timeout=30, poll_frequency=0.5):
        # 1. 先隐式等待元素可见；
        # 2. 定位到该元素，点击元素操作
        self.wait_invisibility_element(locator_name, page_name, timeout, poll_frequency)
        ele = self.find(locator_name, page_name)
        self._logger.info("pageName:{0}---从{1}元素获取本文".format(
            page_name,
            locator_name
        ))
        try:
            value = ele.text  # 获取元素文本值
        except Exception as e:
            self._logger.error("pageName:{0}---从{1}元素获取文本失败！".format(
                page_name,
                locator_name
            ))
            self.save_screeshot(page_name)
            raise
        else:
            self._logger.info("pageName:{0}---从{1}元素获取到本文值:{2}".format(
                page_name,
                locator_name,
                value
            ))
            return value

# 获取该元素的属性
    def get_element_attr(self, locator_name, attr_name, page_name, timeout=30, poll_frequency=0.5):
        # 1. 先隐式等待元素可见；
        # 2. 定位到该元素，点击元素操作
        self.wait_contains_element(locator_name, page_name, timeout, poll_frequency)
        ele = self.find(locator_name)
        self._logger.info("pageName:{0}---{1}元素获取属性值".format(
            page_name,
            locator_name
        ))
        try:
            # 获取该元素的属性
            attr_value = ele.get_attribute(attr_name)
        except Exception as e:
            # 当获取元素属性
            self._logger.error("pageName:{0}---该元素{1}获取属性失败,原因:{2}".format(
                page_name,
                locator_name,
                e
            ))
            self.save_screeshot(page_name)
            raise
        else:
            # 记录下获取的属性
            self._logger.info("pageName:{0}---该元素{1}获取属性值：{2}".format(
                page_name,
                locator_name,
                attr_name
            ))
            return attr_name

# 切换窗口
    def switch_window(self, value):
        time.sleep(3)
        # 获取到当前的宽口
        window = self._driver.window_handles
        self._logger.info("切换窗口到{0}".format(window[value]))
        try:
            self._driver.switch_to.window(window[value])
        except Exception as e:
            self._logger.error("切换窗口失败！原因:{0}".format(e))