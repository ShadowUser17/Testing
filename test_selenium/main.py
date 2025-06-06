import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def get_driver() -> any:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Remote(
        command_executor=os.environ.get("SELENIUM_URL", "http://selenium.docker:4444/wd/hub"),
        options=chrome_options
    )

driver = get_driver()
driver.set_window_size(1280, 720)
print("Start session:", driver.session_id)

# driver.get("https://www.google.com/")
# print("Open", driver.current_url)

# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("kali linux")
# elem.send_keys(Keys.RETURN)

# driver.close()
