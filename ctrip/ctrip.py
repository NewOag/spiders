import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

url = "https://hotels.ctrip.com/hotels/list?checkin=2023/12/08&checkout=2023/12/09"

# url = "https://hotels.ctrip.com/hotels/list?countryId=78&city=228&checkin=2023/12/12&checkout=2023/12/13&optionId=228&optionType=IntlCity&directSearch=0&display=&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0&intl=1"

city_list = ["北海道", "青森县", "岩手县", "宫城县", "秋田县", "山形县", "福岛县", "茨城县", "栃木县", "群马县",
             "埼玉县", "千叶县", "东京都", "神奈川县", "新潟县", "富山县", "石川县", "福井县", "山梨县", "长野县",
             "岐阜县", "静冈县", "爱知县", "三重县", "滋贺县", "京都府", "大阪府", "兵库县", "奈良县", "和歌山县",
             "鸟取县", "岛根县", "冈山县", "广岛县", "山口县", "德岛县", "香川县", "爱媛县", "高知县", "福冈县",
             "佐贺县", "长崎县", "熊本县", "大分县", "宫崎县", "鹿儿岛县", "冲绳县"]
city_list.reverse()

index = 0


def main():
    for city_name in city_list:
        scrap_one_city(city_name)


def scrap_one_city(city_name):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=C:\\Users\\gaowen013\\AppData\\Local\\Google\\Chrome\\Spider Data\\")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("window-size=1920,1080")

        # options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        # user_ag = UserAgent().chrome
        # options.add_argument('user-agent=%s' % user_ag)
        options.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome("./drivers/chromedriver.exe", options=options)

        with open("./ctrip/stealth.min.js", 'r') as f:
            js = f.read()
        # 调用函数在页面加载前执行脚本
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})


        init_script = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});
"""
        driver.execute_script(init_script)

        driver.get(url)
        input()

        driver.implicitly_wait(2)
        while driver.current_url[0:20] != url[0:20]:
            driver.get(url)
        driver.implicitly_wait(2)

        input_area: WebElement = driver.find_element(by=By.XPATH,
                                                     value="//div[@class='list-search-container']/ul[1]/li[1]/div[1]/div[1]/input")
        input_area.clear()
        input_area.send_keys(city_name)
        driver.implicitly_wait(5)
        time.sleep(1.5)

        input_keyword = driver.find_element_by_id("keyword")
        input_keyword.click()
        input_keyword.send_keys("")

        search_button: WebElement = driver.find_element(by=By.XPATH,
                                                        value="//div[@class='list-search-container']/ul/li[last()]/button")
        search_button.click()
        time.sleep(1.5)
        driver.implicitly_wait(5)

        scroll_script = "window.scrollTo(0,document.body.scrollHeight-100)"
        while find_next(driver) is None:
            driver.execute_script(scroll_script)
            time.sleep(1.5)
        print('scroll end')

        while not exist_end(driver):
            next_button = find_next(driver)
            if next_button is not None:
                next_button.click()
            time.sleep(1.5)
            if next_button is None:
                break

        parse_contents(driver, find_contents(driver))
        print(len(driver.find_elements(by=By.XPATH,
                                       value="//div[@class='list-content']/ul/li")))

    finally:
        if driver is not None:
            driver.quit()
            print("driver quit")


def exist_end(driver) -> bool:
    try:
        nothing = driver.find_element_by_xpath("//p[@class='nothing']")
        return nothing is not None
    except NoSuchElementException:
        print('next')
        return False
    finally:
        pass


def find_next(driver):
    try:
        return driver.find_element(by=By.XPATH, value="//div[@class='list-btn-more']/div[@class='btn-box']")
    except NoSuchElementException:
        print('end')
        return None
    finally:
        pass


def find_contents(driver) -> list[WebElement]:
    return driver.find_elements(by=By.XPATH,
                                value="//div[@class='list-content']/ul/li")


def parse_contents(driver, contents: list[WebElement]):
    global index
    all_content = []
    print(len(contents))
    for i, element in enumerate(contents[4:]):
        try:
            res = dict()
            path = str.format("//div[@class='list-content']/ul/li[{}]/div/div/div/div[@class='left']", i + 5)
            left = element.find_element_by_xpath(path)

            name_path = "/div[@class='info']/div[1]/div/span"
            ads_path = "/div[@class='info']/div[2]/p/span[1]"
            tags_path = "/div[@class='info']/div[3]/span"
            encourage_path = "/div[@class='info']/div[4]"
            name = left.find_element_by_xpath(path + name_path)
            ads = left.find_element_by_xpath(path + ads_path)
            tags = left.find_elements_by_xpath(path + tags_path)
            encourage = left.find_element_by_xpath(path + encourage_path)

            res["name"] = name.text
            res["ads"] = ads.text
            tag_list = []
            for tag in tags:
                if not tag.text.isspace() and tag.text != "":
                    tag_list.append(tag.text)
            res["tags"] = tag_list
            res["encourage"] = encourage.text

            right = element.find_element_by_xpath("//div[@class='right']")
            describe = right.find_element_by_xpath("//div[@class='describe']")
            score = right.find_element_by_xpath("//div[@class='score']")
            # price = right.find_element_by_xpath("//span[@class='priceInfo']/span[@class='real-price font-bold']")
            price = right.find_element_by_xpath(
                "//div[@class='list-card-price']/div[@class='price-area']/p/span[@class='priceInfo']/span[@class!='tax' and @class!='line-price' and @class!='price-qi']")

            res["describe"] = describe.text.replace("\n", " ")
            res["score"] = score.text
            res["price"] = price.text

            # map_path = "/div[@class='info']/div[2]/p/span[1]"
            # map_button = driver.find_element_by_xpath(path + map_path)
            # map_button.click()
            #
            # map_addr = driver.find_element_by_xpath("//p[@class='detail-map-list_position']")
            # res["addr"] = map_addr.text

            # close_button = driver.find_element_by_xpath("//i[@type='close']")
            # close_button.click()
            # time.sleep(0.5)

            print(i, res)
            all_content.append(res)
        except NoSuchElementException as e:
            print('error: ', e)
        finally:
            pass
    time.sleep(1.5)
    print(json.dumps(all_content, ensure_ascii=False))
    with open('./data/' + city_list[index] + '.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(all_content, ensure_ascii=False))
    index += 1


if __name__ == "__main__":
    main()
