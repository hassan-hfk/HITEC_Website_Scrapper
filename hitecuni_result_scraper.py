import selenium, time, warnings, logging
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome()
driver.get("https://hitecuni.edu.pk/StudentFacilitations/Result.aspx")

def navigate_MainPage_to_SemesterPage(roll_number):
    text_box = driver.find_element(By.ID, "ContentPlaceHolder_AboutContentPlaceHolder_registrationNoTextBox")
    text_box.send_keys(roll_number)
    text_box_submit_button = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_submitButton")
    text_box_submit_button.click()
    time.sleep(0.5)
def navigate_to_main_page():
    check_another_result_button = driver.find_element(By.ID, "ContentPlaceHolder_AboutContentPlaceHolder_submitButton")
    check_another_result_button.click()
    pass

def get_semester_info(roll_no):
    semester = []
    roll_number = []
    duration = []
    declaration = []
    subjects = []
    bio_data = []
    semester_table_elements = driver.find_elements(By.XPATH, '//*[@id="ContentPlaceHolder_AboutContentPlaceHolder_semesterPanel"]/table/tbody/tr')
    semester_table_elements.pop(0)
    for element in semester_table_elements:
        temp = element.find_element(By.XPATH,f'.//td[1]')
        semester.append(temp.text)
        temp = element.find_element(By.XPATH,f'.//td[2]')
        duration.append(temp.text)
        temp = element.find_element(By.XPATH,f'.//td[3]')
        declaration.append(temp.text)
        roll_number.append(roll_no)
    pass

def navigate_SemesterPage_to_ResultPage():
    pass

def navigate_ResultPage_to_Semester_Page():
    pass

def Result_info():
    pass
navigate_MainPage_to_SemesterPage("20-EE-008")
get_semester_info("20-EE-008")