from selenium.webdriver.common.by import By  # 定位元素
from selenium import webdriver  # 驱动会话
from selenium.webdriver.support.wait import WebDriverWait  # 等待策略
from selenium.common.exceptions import NoSuchElementException  # 异常处理
from selenium.common.exceptions import TimeoutException
import time


class Crawler:

    def __init__(self):
        """
            该方法用于初始化驱动，设置启动参数
            创建工作链接和需求列表存储爬取的数据
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.job_link = []
        self.job_command = []

    def __del__(self):
        self.driver.close()

    def login_(self):
        """
            该方法用于打开登录页面进行扫码登录
        """
        self.driver.get('https://www.zhipin.com/web/user/?ka=header-login')
        time.sleep(10)

    def open_(self):
        """
            该方法用于爬取10个网页的链接和需求
        """
        self.login_()
        for i in range(1, 11):
            time.sleep(1)
            print(f"正在爬取第{i}页内容")
            self.driver.get(
                f'https://www.zhipin.com/web/geek/job?query=Python%E7%88%AC%E8%99%AB&city=101200100&page={i}')
            WebDriverWait(self.driver, timeout=20).until(lambda d: self.driver.find_element(By.CSS_SELECTOR, '#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > ul > li:nth-child(1) > div.job-card-body.clearfix > a'))
            self.get_link()

    def get_link(self):
        """
            该方法用于获取网页中的工作链接
            设置无元素异常和等待超时异常
            最后将获取的链接添加到列表中
        """
        for i in range(1, 31):
            time.sleep(1)
            try:
                link = self.driver.find_element(By.CSS_SELECTOR, f'#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > ul > li:nth-child({i}) > div.job-card-body.clearfix > a').get_attribute("href")
                print(link, end='\n')
            except NoSuchElementException:
                print("无法获取该元素")
            except TimeoutException:
                print("获取超时")
            else:
                self.job_link.append(link)

    def get_command(self):
        """
            该方法用于打开获取的每个链接
            获取每个网页的工作要求
            设置无元素和超时异常处理
            将获取的需求添加到列表中
        """
        for i in self.job_link:
            self.driver.get(i)
            time.sleep(1)
            try:
                WebDriverWait(self.driver, timeout=20).until(lambda d: self.driver.find_element(By.CSS_SELECTOR, '#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text'))
                command = self.driver.find_element(By.CSS_SELECTOR, '#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text').text
                print(command, end='\n')
            except NoSuchElementException:
                print("无法获取该元素")
            except TimeoutException:
                print("获取超时")
            except UnicodeError:
                print("未知编码")
            else:
                self.job_command.append(command)

    def save_(self):
        """
            该方法用于保存获取到的工作需求
        """
        with open("D:\\command.txt", "a+") as f:
            for i in self.job_command:
                try:
                    f.write(i + '\n\n\n')
                except UnicodeError:
                    print("未知编码\n")

    def action(self):
        self.open_()
        self.get_command()
        self.save_()


a = Crawler()
a.action()
