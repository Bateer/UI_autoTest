# 基于selenium+Pytest+Allure的webUI自动化(后续之间更新添加appium，接口)
该UI自动化框架主要是使用到selenium、Pytest、Allure等框架构建：
1. selenium对web进行操作驱动
2. Pytest测试框架来搭建主要流程
3. Allure美化测试结果
4. logger记录下每次操作的日志行为
5. 采用PageObject模式是页面元素更容易管理

## 安装python相关依赖
在requirement.txt中记录了所有所需第三方库，terminal/cmd中直接执行以下命令
```
pip install -r requirements.txt
```

## 安装Allure2相关
github地址：https://github.com/allure-framework/allure2<br>
下载之后，安装在本地，并且给allure配置环境变量，运行查看是否成功
![allure环境配置](file:///C:/Users/Yu/Desktop/allure%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE.png)

## 执行实例
安装配置好第三方依赖以及allure之后，直接运行main
生成日志，以及相关测试报工：
1. 日志以及测试报告所在目录
![目录](file:///C:/Users/Yu/Desktop/%E7%9B%AE%E5%BD%95.png)
2. 根据不同的等级打印日志文件
![日志](file:///C:/Users/Yu/Desktop/%E6%97%A5%E5%BF%97.png)
3. 生成的allure测试报告
![allure报告](file:///C:/Users/Yu/Desktop/allure%E6%8A%A5%E5%91%8A.png)
## 持续更新
后续也可加入结合Jenkins


