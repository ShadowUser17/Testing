import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def get_driver() -> any:
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    return webdriver.Remote(
        command_executor=os.environ.get("SELENIUM_URL", "http://selenium.docker/wd/hub"),
        options=chrome_options
    )

driver = get_driver()
print("Start session:", driver.session_id)

# driver.get("https://www.google.com/")
# print("Open", driver.current_url)

# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("kali linux")
# elem.send_keys(Keys.RETURN)

# driver.close()
