from selenium import webdriver
import chromedriver_autoinstaller

Instance = None
isHeadless = False
CHROME_DRIVER = './chromedriver/chromedriver'

def Initialize(headless = False):
    global Instance
    global isHeadless
    isHeadless = headless
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--log-level=3")
        options.add_argument("headless")
        options.add_experimental_option('excludeSwitches',['enable-logging']);
    # Instance = webdriver.Chrome(executable_path = CHROME_DRIVER, chrome_options=options)
    Instance = webdriver.Chrome(chrome_options=options)
    return Instance

def CloseDriver():
    global Instance
    global isHeadless
    if not isHeadless:
        print("Closing Browser...!")
    Instance.quit()