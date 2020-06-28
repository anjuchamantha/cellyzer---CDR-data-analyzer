from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium .webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

chromedriver= "C:\\Users\\Malith\\Downloads\\chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get("http://127.0.0.1:8050")

element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "add-cell-records-dataset")))
element.click()

call = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "call_card")))
call.click()

####### add call dataset
call_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
call_name.send_keys("E:\\Project\\demo_datasets\\test_data\\calls.csv")
choose_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data_call")))
choose_call.send_keys("Call")
add_call = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "adding_call")))
add_call.click()

###### go to dataset page after adding call dataset
go_dataset_page = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "add-cell-records-dataset")))
go_dataset_page.click()
driver.refresh()

#### visit "Call" call dataset
visit_call = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "Call")))
visit_call.click()

#### show call data
show_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_show_call")))
show_call.click()
view_call_data =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "view")))
view_call_data.click()
driver.execute_script("window.history.go(-1)")
driver.refresh()

##### show all call users
call_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_users")))
call_users.click()
view_call_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "get_users")))
view_call_users.click()
driver.execute_script("window.history.go(-1)")
driver.refresh()

# ##### show connected users for given input
# connected_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_connected")))
# connected_users.click()
# select_user_call_conn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "but_select_user")))
# select_user_call_conn.click()
# input1 =  WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='search']")))
# input1.send_keys("8d27cf2694")
# get_connected_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "connected_users")))
# get_connected_users.click()
# driver.execute_script("window.history.go(-1)")
# driver.refresh()

# ###### show call record between 2 users
# call_record_2_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_records")))
# call_record_2_users.click()
# select_user_call_2user = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select_user_records_2_user")))
# select_user_call_2user.click()
# call_record_input1 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "search_2")))
# call_record_input1.send_keys("8d27cf2694")
# call_record_input2 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "search_3")))
# call_record_input2.send_keys("7187432175")
# get_call_record_2_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "record_users")))
# get_call_record_2_users.click()
# driver.execute_script("window.history.go(-1)")
# driver.refresh()

# ###### show close contacts for given input
# close_contacts =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_close")))
# close_contacts.click()
# select_user_close_contact = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select_user_close_contact")))
# select_user_close_contact.click()
# close_contacts_input1 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_3")))
# close_contacts_input1.send_keys("8d27cf2694")
# close_contacts_input2 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "contact")))
# close_contacts_input2.send_keys("2")
# get_close_contacts =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "close_contacts")))
# get_close_contacts.click()
# driver.execute_script("window.history.go(-1)")
# driver.refresh()

# ##### show ignored calls
# ignored_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_ignored_call")))
# ignored_call.click()
# select_user_ignored_call = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select_user_ignore_call")))
# select_user_ignored_call.click()
# ignored_call_input =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_5")))
# ignored_call_input.send_keys("8d27cf2694")
# get_ignored_call =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ignore_call")))
# get_ignored_call.click()
# driver.execute_script("window.history.go(-1)")
# driver.refresh()

# ##### show active time of user
# active_time =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_active_time")))
# active_time.click()
# select_user_active_time = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select_user_active_time")))
# select_user_active_time.click()
# active_time_input =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_4")))
# active_time_input.send_keys("8d27cf2694")
# get_active_time =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "active_time")))
# get_active_time.click()
# driver.execute_script("window.history.go(-1)")
# driver.refresh()

##### visualize connection between all call users
visualize_connection =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_call_visu_connection")))
visualize_connection.click()
# select_user_call_visu_conn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select_user_visu_conn")))
# select_user_call_visu_conn.click()
view_visualize_connection =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visualize_connection")))
view_visualize_connection.click()

##### go to dataset page after visualize connection of call users
element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "add-cell-records-dataset")))
element.click()
driver.refresh()

################################
message = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "message_card")))
message.click()

####### add message dataset
message_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
message_name.send_keys("E:\\Project\\demo_datasets\\test_data\\messages.csv")
choose_message =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data_message")))
choose_message.send_keys("Message")
add_message = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "adding_message")))
add_message.click()

###### go to dataset page after adding message dataset
go_dataset_page_message = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "add-cell-records-dataset")))
go_dataset_page_message.click()
driver.refresh()

#### visit "Message" message dataset
visit_message = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "Message")))
visit_message.click()
driver.refresh()

#### show message data
show_message =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_message_data")))
show_message.click()
view_message_data =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "view_message")))
view_message_data.click()
driver.execute_script("window.history.go(-1)")
driver.refresh()

##### show all message users
message_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_message_users")))
message_users.click()
view_message_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "get_message_users")))
view_message_users.click()
driver.execute_script("window.history.go(-1)")
driver.refresh()

# ###### show message record between 2 users
# message_record_2_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_message_records_2")))
# message_record_2_users.click()
# message_record_input1 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "message_user2")))
# message_record_input1.send_keys("7681546436")
# message_record_input2 =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "message_user3")))
# message_record_input2.send_keys("7641036117")
# get_message_record_2_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "record_message_users")))
# get_message_record_2_users.click()
# driver.execute_script("window.history.go(-1)")

##### visualize connection between all message users
visu_conn_message =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_message_visualization")))
visu_conn_message.click()
view_visu_conn_message =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visualize_message_connection")))
view_visu_conn_message.click()
driver.execute_script("window.history.go(-1)")
driver.refresh()

# ##### show connected message users for given input
# connected_message_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_message_connected")))
# connected_message_users.click()
# select_msg_user_call_conn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select_msg_user_connected")))
# select_msg_user_call_conn.click()
# input_message =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='user_message']")))
# input_message.send_keys("8d27cf2694")
# get_connected_message_users =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "connected_message_users")))
# get_connected_message_users.click()
# driver.execute_script("window.history.go(-1)")
# driver.refresh()

element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "add-cell-records-dataset")))
element.click()

#############################
cell = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cell_card")))
cell.click()

####### add cell dataset
cell_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
cell_name.send_keys("E:\\Project\\demo_datasets\\test_data\\antennas.csv")
# cell_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "filepath_cell")))
# cell_name.send_keys("C:\\Users\\Malith\\Downloads\\cellyzer---CDR-data-analyzer\\dataset\\sample data\\csv data\\antennas.csv")
choose_cell =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "upload-data_cell")))
choose_cell.send_keys("Cell")
# choose_call_cell =  Select(WebDriverWait(driver, 20).until(EC.element_located_to_be_selected((By.ID, "select_call"))))
# choose_call_cell.select_by_value('Call')
choose_call_cell =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='select_call']")))
choose_call_cell.send_keys("Call")
# choose_call_cell =  Select(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select_call"))))
# choose_call_cell.select_by_visible_text('Call')
add_cell = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "show_cell_dash")))
add_cell.click()

# #### visit "Cell" cell dataset
# visit_cell = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "Cell")))
# visit_cell.click()

# #### show cell data
# show_cell =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_cell_data")))
# show_cell.click()
# view_cell_data =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "view_cell")))
# view_cell_data.click()
# driver.execute_script("window.history.go(-1)")

# ##### show cell record id
# cell_id =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_cell_id")))
# cell_id.click()
# input_cell_id =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "cell_id")))
# input_cell_id.send_keys("2")
# view_cell_id =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "records_cell")))
# view_cell_id.click()
# driver.execute_script("window.history.go(-1)")

# ##### show population visualize
# population_visualize =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_population")))
# population_visualize.click()
# get_population =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "population_button")))
# get_population.click()
# driver.execute_script("window.history.go(-1)")

# ##### show trip visualization of given input
# trip_visualization =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "visu_trip_visualization")))
# trip_visualization.click()
# trip_user =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "trip_user")))
# trip_user.send_keys("7681546436")
# get_trip_visualization =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "trip_visualize_button")))
# get_trip_visualization.click()
# driver.execute_script("window.history.go(-1)")