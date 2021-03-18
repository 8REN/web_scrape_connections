#!/usr/bin/env python
# coding: utf-8

# # automate login 
#  
# assigning webdriver instance outside of automated login function 

# In[5]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# In[2]:


# create webdriver instance
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


# In[3]:


def sign_in(email, password):
#     this function automates login process on linkedin, 
#     provide email and password as strings
    driver = webdriver.Chrome(PATH)
    # webdriver gets page
    driver.get("https://www.linkedin.com/")
    # pause for page to load
    time.sleep(3)
    # locate and send login email and password
    driver.find_element_by_id("session_key").send_keys(email)
    driver.find_element_by_id("session_password").send_keys(password)
    driver.find_element_by_class_name("sign-in-form__submit-button").click()


# In[6]:


# arguments input as strings for email and password for linkedin website
sign_in('email@gmail.com', 'password')


# # automate login 
# 
# assigning webdriver instance inside automated login function

# In[ ]:


def get_driver_login(email, password, PATH):
#     this function automates login process on linkedin, 
#     provide email and password as strings
#     assign webdriver instance to driver variable using function
    driver = webdriver.Chrome(PATH)
    time.sleep(5)
    # webdriver gets page
    driver.get("https://www.linkedin.com/")
    # pause for page to load
    time.sleep(3)
    # locate and send login email and password
    driver.find_element_by_id("session_key").send_keys(email)
    driver.find_element_by_id("session_password").send_keys(password)
    driver.find_element_by_class_name("sign-in-form__submit-button").click()
    return driver


# In[ ]:


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = get_driver_login('email@gmail.com', 'password1!', PATH)

