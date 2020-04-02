# -*- Coding: utf-8 -*-
# Author: Yu

from selenium import webdriver
from Common.base_page import BasePage
from selenium.webdriver.common.by import By
from time import sleep


class BaiPage(BasePage):
    _base_url = "https://www.baidu.com/"

    def search_handle(self, key):
        search_loc = (By.ID, "kw")
        self.find(search_loc).send_keys(key)
        self.find((By.ID, "su"), page_name='百度首页').click()
        return self

    def close(self):
        sleep(2)
        self._driver.quit()