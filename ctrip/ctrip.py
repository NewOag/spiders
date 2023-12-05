import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# url = "https://hotels.ctrip.com/hotels/list"

url = "https://hotels.ctrip.com/hotels/list?countryId=78&city=228&checkin=2023/12/06&checkout=2023/12/07&optionId=228&optionType=IntlCity&directSearch=0&display=%E4%B8%9C%E4%BA%AC&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0&intl=1"


def main():
    driver = None
    try:
        driver = webdriver.Chrome("./drivers/chromedriver.exe")

        driver.get(url)

        driver.implicitly_wait(2)
        while driver.current_url[0:20] != url[0:20]:
            driver.get(url)
        driver.implicitly_wait(2)

        # input_area: WebElement = driver.find_element(by=By.XPATH,
        #                                              value="//div[@class='list-search-container']/ul[1]/li[1]/div[1]/div[1]/input")
        # input_area.clear()
        # input_area.send_keys("东京, 日本")

        search_button: WebElement = driver.find_element(by=By.XPATH,
                                                        value="//div[@class='list-search-container']/ul/li[last()]/button")

        search_button.click()
        driver.implicitly_wait(5)

        # contents: list[WebElement] = find_contents(driver)
        # parse_contents(contents)

        scroll_script = "window.scrollTo(0,document.body.scrollHeight-100)"
        while find_next(driver) is None:
            driver.execute_script(scroll_script)
            time.sleep(3)

        for _ in range(20):
            next_button = find_next(driver)
            next_button.click()
            time.sleep(2)

        parse_contents(find_contents(driver))
        print(len(driver.find_elements(by=By.XPATH,
                                       value="//div[@class='list-content']/ul/li")))

    finally:
        if driver is not None:
            driver.quit()
            print("driver quit")


def find_next(driver):
    return driver.find_element(by=By.XPATH, value="//div[@class='list-btn-more']/div[1]")


def find_contents(driver) -> list[WebElement]:
    return driver.find_elements(by=By.XPATH,
                                value="//div[@class='list-content']/ul/li")


def parse_contents(contents: list[WebElement]):
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

            res["describe"] = describe.text.replace("\n", " ")
            res["score"] = score.text

            print(i, res)
            all_content.append(res)
        except NoSuchElementException:
            pass
        finally:
            pass
    time.sleep(10)
    print(json.dumps(all_content, ensure_ascii=False))


if __name__ == "__main__":
    main()
