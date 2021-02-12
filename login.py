from selenium import webdriver
def sign_in(email, password):
#     this function automates login process on linkedin, 
#     provide email and password as strings
    
    # webdriver gets page
    driver.get("https://www.linkedin.com/")
    # pause for page to load
    time.sleep(3)
    # locate and send login email and password
    driver.find_element_by_id("session_key").send_keys(email)
    driver.find_element_by_id("session_password").send_keys(password)
    driver.find_element_by_class_name("sign-in-form__submit-button").click()
    return driver.current_url