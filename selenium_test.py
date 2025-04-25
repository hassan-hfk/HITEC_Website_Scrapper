import selenium, time, warnings, logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless=new")
warnings.filterwarnings('ignore')
logging.getLogger("tensorflow").setLevel(logging.ERROR)
#from selenium.webdriver.chrome.service import Service
#service = Service(executable_path=r"C:\Users\Hassan Farooq Khan\Desktop\Hassan-Dev-Test\chromedriver-win64\chromedriver.exe")
semester = []
roll_number_list = []
missing_roll_number = []
Batch = ["19","20","21","22"]
Department = ["EE", "ME"]
driver = webdriver.Chrome(options=options)
driver.get("https://hitecuni.edu.pk/StudentFacilitations/Result.aspx")
def get_semester_info(department, batch, roll_number):

    roll_number = batch+"-"+department+"-"+roll_number
    registration_number_box = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_registrationNoTextBox")
    registration_number_box.clear()
    registration_number_box = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_registrationNoTextBox")
    registration_number_box.send_keys(roll_number)

    registration_number_box_button = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_submitButton")
    registration_number_box_button.click()
    time.sleep(0.25)
    
    semester_information_element = driver.find_element(By.XPATH,'//*[@id="ContentPlaceHolder_AboutContentPlaceHolder_semesterPanel"]/table/tbody')
    semester_information = semester_information_element.find_elements(By.XPATH,'.//tr/td[1]')
    for i in semester_information:
        if not i.text == "Semester":
            semester.append(i.text)
            roll_number_list.append(roll_number)
    #print(semester)
    
    registration_number_box_button = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_submitButton")
    registration_number_box_button.click()
    time.sleep(0.25)

def QA_missing_roll_number(missing_roll_number_list):
    semester = []
    roll_number_list = []
    for roll_number in missing_roll_number_list:
        try:    
            registration_number_box = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_registrationNoTextBox")
            registration_number_box.clear()
            registration_number_box = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_registrationNoTextBox")
            registration_number_box.send_keys(roll_number)
            registration_number_box_button = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_submitButton")
            registration_number_box_button.click()
            time.sleep(2)
            semester_information_element = driver.find_element(By.XPATH,'//*[@id="ContentPlaceHolder_AboutContentPlaceHolder_semesterPanel"]/table/tbody')
            semester_information = semester_information_element.find_elements(By.XPATH,'.//tr/td[1]')
            for i in semester_information:
                if not i.text == "Semester":
                    semester.append(i.text)
                    roll_number_list.append(roll_number)
            registration_number_box_button = driver.find_element(By.ID,"ContentPlaceHolder_AboutContentPlaceHolder_submitButton")
            registration_number_box_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Exception arrised : Roll No {roll_number}")
    return pd.DataFrame({"Roll_No": roll_number_list, "Semester": semester})
for dep in Department:
    for batch in Batch: 
        print(f"Scrapping Semester Info for {batch}-{dep} Started \n")
        semester = []
        roll_number_list = []
        for i in range(150):
            if i < 10:
                temp_roll_number = "00"+str(i)
            else:
                temp_roll_number = "0"+str(i)
            try:
                get_semester_info(dep,batch,temp_roll_number)
            except Exception as e:
                #print(f"Exception arrised : Roll No {batch}-{dep}-{temp_roll_number}")
                missing_roll_number.append(f"{batch}-{dep}-{temp_roll_number}")
        df = pd.DataFrame({"Roll_No": roll_number_list, "Semester": semester})
        print(f"{df.shape[0]} Entities Found.")
        print(f"{len(missing_roll_number)} Missing Roll Numbers Found -> QA Initiates now for {batch}-{dep}")
        stack = QA_missing_roll_number(missing_roll_number)
        if stack.shape[0] > 0:
            print(f"QA Succesfull, {stack.shape[0]} Entities Founded. Now Adding them into main CSV file")
            df = pd.concat([df,stack], ignore_index=True)
        else:
            print("QA Succesfull, No Entities Founded")
            df.to_csv(f"{batch}_{dep}_Semester.csv")
            df = pd.DataFrame({"Missing Roll Numbers": missing_roll_number})
            df.to_csv(f"{batch}_{dep}_Missing_Roll_Number.csv")
time.sleep(1000)
driver.quit()
#ContentPlaceHolder_AboutContentPlaceHolder_registrationNoTextBox

