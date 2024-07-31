from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import functions

## making driver
options = Options()
options.add_argument("--enable-chrome-browser-cloud-management")
options.add_experimental_option("detach", True) # not to close broswer after task
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
driver.maximize_window()

## running tasks
functions.prim_login(driver)
functions.get_course_history_and_links(driver)
functions.go_every_course_and_scrap_assignments(driver)