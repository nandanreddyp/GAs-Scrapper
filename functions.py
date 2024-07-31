import requests, json, csv, os, time
from selenium.webdriver.common.by import By

def initialize():
    if not os.path.exists('venv'): print('Please install virtual env and install the requirements'); os.exit()
    if not os.path.exists('data/cookie.json'):
        with open('data/cookie.json','w') as f:
            f.write('{}')
        data = read_Json()
        data['session']=''; data['email']=input('Please enter your email id: '); data['password']=input('Please enter your password: ')
        write_Json(data)

def read_Json():
    with open('data/cookie.json','r') as f:
        data = json.load(f)
    return data

def write_Json(data):
    with open('data/cookie.json','w') as f:
        json.dump(data,f)
    return 'Dumped'

def is_logged():
    session_value = None; url = "https://ds.study.iitm.ac.in/student_dashboard/current_courses"
    cookies = {
        'session': read_Json()['session']
    }
    response = requests.get(url, cookies=cookies)
    if 'Sign-in' in response.text:
        return False
    return True

def prim_login(driver):
    if not is_logged():
        print('Please login in poped up browser')
        # Navigate to the login page
        driver.get("https://ds.study.iitm.ac.in/auth/login")
        initial_url = driver.current_url
        redirecting = True
        while redirecting:
            new_url = driver.current_url
            redirecting = (new_url == initial_url)
        # Write cookie information to a file
        session_cookie = driver.get_cookie('session')
        data = read_Json()
        data['session'] = session_cookie['value']
        write_Json(data)
    else:
        print('Already logged in :-)')
        driver.get('https://ds.study.iitm.ac.in/auth/login')
        driver.add_cookie({'name' :'session' , 'value' : read_Json()['session']})
        # driver.refresh()
        driver.get("https://ds.study.iitm.ac.in/student_dashboard/current_courses")
    return 

def get_course_history_and_links(driver):
    driver.get("https://ds.study.iitm.ac.in/student_dashboard/student_courses")
    completed_container = driver.find_element(By.CLASS_NAME, 'completed_courses')
    child_elements = completed_container.find_elements(By.CLASS_NAME, 'course_item')
    with open('data/completed_courses.txt','w') as f:
        for child in child_elements:
            anchor = child.find_element(By.TAG_NAME,'a')
            f.write(anchor.text+'\t')
            f.write(anchor.get_attribute('href')+'\n')
    file = open('data/completed_courses.txt','r')
    links = csv.reader(file,delimiter='\t')
    links_file = open('data/completed_courses_links.txt','w')
    for link in links:
        driver.get(link[1])
        # going to course history
        parent = driver.find_element(By.CLASS_NAME, 'courses-history')
        anchor = parent.find_element(By.TAG_NAME,'a')
        history_link = anchor.get_attribute('href')
        links_file.write(f'{link[0]}\t{history_link}\n')
        driver.get(history_link)
    return 

def sec_login(driver,course_url):
    redirecting = True
    time.sleep(5)
    main_page = driver.current_window_handle
    button_element = driver.find_element(By.CLASS_NAME, 'google-login-btn')
    button_element.click()
    time.sleep(4) 
    for handle in driver.window_handles: 
        if handle != main_page: 
            login_page = handle 
    driver.switch_to.window(login_page)
    time.sleep(3)
    email = read_Json()['email']
    password = read_Json()['password']
    driver.find_element(By.CSS_SELECTOR, '#identifierId').send_keys(email)
    # driver.find_element_by_xpath('//*[@id ="identifierId"]').send_keys(email) 
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(3)
    # driver.find_element(By.NAME, 'input').send_keys(password)
    driver.find_element(By.CSS_SELECTOR,'input[aria-label="Enter your password"]').send_keys(password)
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    # switch to main window
    driver.switch_to.window(main_page)
    while redirecting:
        new_url = driver.current_url
        redirecting = (course_url != new_url)

def go_every_course_and_scrap_assignments(driver):
    file = open('data/completed_courses_links.txt','r')
    links = csv.reader(file,delimiter='\t')
    for link in links:
        course_url = link[1]
        driver.get(link[1])
        # if course want to login
        if course_url != driver.current_url:
            sec_login(driver,course_url)
        # scarping html files of assignments
        scrap_assignments(driver); break
    return

def scrap_assignments(driver):
    required_text = {'Graded Assignment'}
    # parent div class  = 'units__items ng-star-inserted' week
    # child in that parent = 'units__sublist' sub lists
    # class = 'units__subitems ng-star-inserted' list items if contains text as we want!
    print('scrapping assignments')
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    time.sleep(10)
    f=open('test_GA.html','w')
    # f.write(driver.page_source)
    # f.close()
    units_list = driver.find_element(By.CSS_SELECTOR, '.units__list')
    units = units_list.find_elements(By.CSS_SELECTOR,'.units__items.ng-star-inserted')
    for unit in units:
        unit.click()
        units_sublist = unit.find_element(By.CSS_SELECTOR,'.units__sublist')
        units_subitems = units_sublist.find_elements(By.CSS_SELECTOR,'.units__subitems')
        for subitem in units_subitems:
            
            clickable = subitem.find_element(By.CSS_SELECTOR,'.units__subitems-text')
            time.sleep(3)
            clickable.click()
    return

