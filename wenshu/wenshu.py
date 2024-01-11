import time

from common.driver import *


def main():
    driver = init()
    # driver = webdriver.Chrome("../drivers/chromedriver")
    url = "https://wenshu.court.gov.cn/"
    # url = "https://image.baidu.com/"
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(10)


if __name__ == '__main__':
    main()
