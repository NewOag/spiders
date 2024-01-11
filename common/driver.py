from selenium import webdriver


def init():
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir=C:\\Users\\gaowen013\\AppData\\Local\\Google\\Chrome\\Spider Data\\")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # options.add_argument("window-size=1920,1080")

    # options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2} # 禁止图片
    # options.add_experimental_option("prefs", prefs)
    # user_ag = UserAgent().chrome
    # options.add_argument('user-agent=%s' % user_ag)
    options.add_experimental_option('useAutomationExtension', False)  # 去掉开发者警告
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome("../drivers/chromedriver", options=options)

    with open("stealth.min.js", 'r') as f:
        js = f.read()
    # 调用函数在页面加载前执行脚本
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})

    init_script = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});
"""
    driver.execute_script(init_script)
    return driver
