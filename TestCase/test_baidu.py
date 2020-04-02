# -*- Coding: utf-8 -*-
# Author: Yu
from PageObject.baidu_PG import BaiPage
import pytest
import allure
from time import sleep

@allure.feature("测试第一个例子")
class Test_First:
    def setup(self):
        self.baiPage = BaiPage()

    @pytest.mark.smoke
    @allure.story("被测场景py")
    def test_01(self):
        self.baiPage.search_handle("selenium")

    def teardown(self):
        self.baiPage.close()


# if __name__ == "__main__":
#     pytest.main()
