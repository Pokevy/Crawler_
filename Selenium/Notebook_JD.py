import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Spider:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.name = []
        self.price = []
        self.cpu = []
        self.ds = []
        self.measure = []
        self.link = []

    def __del__(self):
        self.driver.quit()

    def login_(self):
        """
        用于扫码登录
        :return:
        """
        self.driver.get('https://open.weixin.qq.com/connect/qrconnect?appid=wx827225356b689e24&state=19D2E730B73EA22927E679D356B0A877613D7DB972775B7869495B0D3D64A8FFBB21AAC5EE9D8EF3BE5E83EB56A9B8F1&redirect_uri=https%3A%2F%2Fqq.jd.com%2Fnew%2Fwx%2Fcallback.action%3Fview%3Dnull%26uuid%3D244fea33632f4750b695ff6d54c766b9&response_type=code&scope=snsapi_login#wechat_redirect')
        time.sleep(15)

    def roll_bottom(self):
        """
        控制浏览器慢慢滚动到底部
        :return:
        """
        js = "return action=document.body.scrollHeight"
        height = 0
        new_height = self.driver.execute_script(js)
        while height < new_height:
            for i in range(height, new_height, 2000):
                self.driver.execute_script(f'window.scrollTo(0, {i})')
                time.sleep(0.5)
            height = new_height
            time.sleep(0.5)
            new_height = self.driver.execute_script(js)

    def craw_link(self):
        """
        获取每页商品的链接和价格，存储到类属性中
        :return:
        """
        self.login_()
        for i in range(1, 8, 2):
            time.sleep(1)
            self.driver.get(f'https://search.jd.com/Search?keyword=%E6%B8%B8%E6%88%8F%E6%9C%AC&page={i}')
            self.roll_bottom()
            WebDriverWait(self.driver, timeout=20).until(lambda d: self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[1]/div/div[2]/ul'))
            for j in range(1, 31):
                try:
                    link = self.driver.find_element(By.XPATH,f'//*[@id="J_goodsList"]/ul/li[{j}]/div/div[3]/a').get_attribute('href')
                    price = self.driver.find_element(By.XPATH,f'//*[@id="J_goodsList"]/ul/li[{j}]/div[1]/div[2]/strong/i').text
                except NoSuchElementException as e:
                    print(e)
                except TimeoutException as e:
                    print(e)
                else:
                    # print(link,end='\n')
                    self.link.append(link)
                    self.price.append(price)

    def craw_data(self):
        """
        从类属性中循环抓取每个商品的信息
        使用正则表达式匹配文本
        :return:
        """
        a = len(self.link)
        print(f"共有{a}件商品待爬取")
        c = 1
        for i in self.link:
            time.sleep(1.5)
            try:
                self.driver.get(i)
                WebDriverWait(self.driver, timeout=20).until(lambda d: self.driver.find_element(By.XPATH, '//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]'))
                ul = self.driver.find_element(By.XPATH, '//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]').text
                # print(ul)
                name_pattern = re.compile('商品名称：(.*?)\n')
                cpu_pattern = re.compile('处理器：(.*?)\n')
                ds_pattern = re.compile('显卡型号：(.*?)\n')
                measure_pattern = re.compile('屏幕尺寸：(.*?)\n')
                name = "".join(re.findall(name_pattern, ul)).replace(' ', '')
                cpu = "".join(re.findall(cpu_pattern, ul)).replace(' ', '')
                ds = "".join(re.findall(ds_pattern, ul)).replace(' ', '')
                measure = "".join(re.findall(measure_pattern, ul))
                if len(cpu) == 0:
                    cpu = '未知'
                if len(ds) == 0:
                    ds = '未知'
                if len(measure) == 0:
                    measure = '未知'
            except NoSuchElementException:
                print("获取失败")
            except TimeoutException:
                print("获取超时")
            else:
                print(f"第{c}件产品", name, cpu, ds, measure, end='\n')
                self.name.append(name)
                self.cpu.append(cpu)
                self.ds.append(ds)
                self.measure.append(measure)
                c = c+1

    def save_data(self):
        """
        将每件商品的信息保存至CSV文件中
        :return:
        """
        d = {'名称': self.name, '价格': self.price, 'CPU': self.cpu, '显卡': self.ds, '尺寸': self.measure,
             '链接': self.link}
        df = pd.DataFrame(d)
        df.to_csv('D:\\JD_NoteBook.csv')

    def action(self):
        self.craw_link()
        self.craw_data()
        self.save_data()


a = Spider()
a.action()
