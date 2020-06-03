from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium .webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver= "C:\\Users\\Malith\\Downloads\\chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get("http://127.0.0.1:8050")

element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "add-cell-records-dataset")))
element.click()

call = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "call_card")))
call.click()

call_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "filepath")))
call_name.send_keys("C:\\Users\\Malith\\Downloads\\cellyzer---CDR-data-analyzer\\dataset\\sample data\\csv data\\calls.csv")
choose_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data_call")))
choose_call.send_keys("Call")
add_call = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "adding_call")))
add_call.click()

#### visit "Call" call dataset
visit_call = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "Call")))
visit_call.click()

#### show call data
show_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_show_call")))
show_call.click()
view_call_data =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "view")))
view_call_data.click()
driver.execute_script("window.history.go(-1)")

##### show all call users
call_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_users")))
call_users.click()
view_call_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "get_users")))
view_call_users.click()
driver.execute_script("window.history.go(-1)")

##### show connected users for given input
connected_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_connected")))
connected_users.click()
input1 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "search")))
input1.send_keys("7163185791")
get_connected_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "connected_users")))
get_connected_users.click()
driver.execute_script("window.history.go(-1)")

###### show call record between 2 users
call_record_2_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_records")))
call_record_2_users.click()
call_record_input1 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "search_2")))
call_record_input1.send_keys("7163185791")
call_record_input2 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "search_3")))
call_record_input2.send_keys("7187432175")
get_call_record_2_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "record_users")))
get_call_record_2_users.click()
driver.execute_script("window.history.go(-1)")

###### show close contacts for given input
close_contacts =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_close")))
close_contacts.click()
close_contacts_input1 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_3")))
close_contacts_input1.send_keys("7163185791")
close_contacts_input2 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "contact")))
close_contacts_input2.send_keys("2")
get_close_contacts =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "close_contacts")))
get_close_contacts.click()
driver.execute_script("window.history.go(-1)")

##### show ignored calls
ignored_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_ignored_call")))
ignored_call.click()
ignored_call_input =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_5")))
ignored_call_input.send_keys("7641036117")
get_ignored_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ignore_call")))
get_ignored_call.click()
driver.execute_script("window.history.go(-1)")

##### show active time of user
active_time =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_active_time")))
active_time.click()
active_time_input =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_4")))
active_time_input.send_keys("7163185791")
get_active_time =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "active_time")))
get_active_time.click()
driver.execute_script("window.history.go(-1)")

##### visualize connection between all users
visualize_connection =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_users")))
visualize_connection.click()
view_visualize_connection =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visualize_connection")))
view_visualize_connection.click()

element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "add-cell-records-dataset")))
element.click()

