from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import functions

## making driver
edge_options = Options()
edge_options.add_argument("--enable-chrome-browser-cloud-management")
edge_options.add_experimental_option("detach", True) # not to close broswer after task
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),options=edge_options)
driver.maximize_window()

## running tasks
functions.prim_login(driver)
functions.get_course_history_and_links(driver)
functions.go_every_course_and_scrap_assignments(driver)