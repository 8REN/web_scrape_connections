#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


# In[4]:


import time
import csv
import numpy as np
import pandas as pd
import requests
import re

from IPython.core.display import HTML


# In[5]:


def sign_in(email, password, PATH):
#     this function automates login process on linkedin, 
#     provide email and password as strings
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


# In[6]:


def people_scrape(search_term, num_pages):
        
#                 function to automate search bar, search focus
#                 from your linkedin homepage, collecting data from
#                 search including name, location(secondary_deets), 
#                 headline(primary_deets) from condensed profiles returned from
#                 search results. requires string entry for search term
#                 and int input for number of pages (num_pages) 
#                 that you wish to scrape from results.

    # activate search bar cursor with click
    driver.find_element_by_css_selector("div#global-nav-search ").click()
    time.sleep(2)
    # send keyboard entry "div[id='oc-background-section']")for search terms
    driver.find_element_by_css_selector("input.search-global-typeahead__input").send_keys(search_term)
    # send enter key to activate search
    driver.find_element_by_css_selector("input.search-global-typeahead__input").send_keys(Keys.RETURN)
    # wait for results to load
    driver.implicitly_wait(6)
    #w.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.reusable-search__entity-results-list')))
    element = driver.find_element_by_css_selector('ul.reusable-search__entity-results-list ')
    # scroll to element containing target(people_banner)  allowing ajax elements to load
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.implicitly_wait(5)
   # locate banner under search type results
    people_banner = driver.find_element_by_link_text(f"See all people results")
    # js function to click banner/button to see additional results under jobs, people, or posts                      
    driver.execute_script('arguments[0].click();',people_banner)
    # pause to allow page to load
    driver.implicitly_wait(6)
    # starting with pagination page 1                       
    page_number = 1
    # get current url for page
    current_page_url = driver.current_url

    # set while loop to define pagination and data collection conditions
    while page_number <= num_pages:
        print("Processing page: " + str(page_number))
    # find all results on page
        links = driver.find_elements_by_css_selector("div.entity-result__content ")
   # pause for page load
        time.sleep(2)
    
    # iterate through results
        for l in links:
    # retrieve profile url
            title = l.find_element_by_css_selector("span.entity-result__title a.app-aware-link")
            profile_path = (str(title.get_attribute("pathname")))
    # add to urls list
            url_list.append(profile_path)
    # locating elements containing text needed
            details = l.find_elements_by_css_selector("div.linked-area")
    # the first element has the first three lines of text in the container
            deets = details[0]  
    # split text to assign elements appropriately
            text = deets.get_attribute('innerText').split('\n')
    # retrieve name/add to list
            name = text[0]
            names_list.append(name)
    # retrieve location/add to list   
            loc = text[-1]
            loc_list.append(loc)
     # retrieve headline/add to list
            headline = text[-2]
            headline_list.append(headline)
    # the second element selected contains the 'Current:' job text 
            current_job = details[1]
    # removing the 'Current:' string from text
            current_job = current_job.get_attribute('innerText').split(':')[1]
    # add current job to list
            current_job_list.append(current_job)
        time.sleep(3)
    # navigate using pagination function
        goto_next_page()
        page_number+=1
    # print to verify page during processing
        print(f"attempting to navigate to search results page {page_number}")
        time.sleep(5)
   
    # create dataframe with extracted information and save as csv file
    df = pd.DataFrame()                      
    df['name'] = names_list
    df['url'] = url_list
    df['current_job'] = current_job_list
    df['location'] = loc_list
    df['headline'] = headline_list
    # add complete url information for use in complete profile scraping
    for row in df:
        df['fetch'] = 'https://www.linkedin.com' + df.url + '/'
    df.to_csv(f'{search_term}.csv')
    # verify save
    print(f'{search_term}.csv saved')
    return df


# In[7]:


#function to locate and interact with "next" button at bottom of search
def goto_next_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.find_element_by_css_selector('div.artdeco-pagination')
    go_to_next = driver.find_element_by_css_selector('button[aria-label="Next"]')
    driver.execute_script('arguments[0].click();',go_to_next)


# In[39]:


def get_experience():
    time.sleep(3)
    w = WebDriverWait(driver, 10)
    
    w.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h2.pv-profile-section__card-heading")))
    h2_heading = driver.find_element_by_css_selector(
        "h2.pv-profile-section__card-heading")
    driver.execute_script("arguments[0].scrollIntoView();", h2_heading)
    time.sleep(3)
    # background container
    background = driver.find_element_by_css_selector(
        "div[id='oc-background-section']")
    # scroll background container into view to access elements within
    driver.execute_script("arguments[0].scrollIntoView();", background)
    # wait for section to be accessible
    w.until(EC.presence_of_element_located((By.CSS_SELECTOR,"section#experience-section")))
    # locate element and access it
    exp = background.find_element_by_css_selector(
            "section[id='experience-section']")
    history = exp.find_elements_by_css_selector('li.pv-entity__position-group-pager')
    details = history[0]
    # try/except clause used to locate element to avoid 'element not found' error which halts program
    try:
        pos = details.find_element_by_tag_name(
                'h3').get_attribute('outerText')
    except NoSuchElementException:
        pos = 'nan'

    try:
        company = details.find_element_by_tag_name(
                'p.pv-entity__secondary-title').get_attribute('innerText')
    except NoSuchElementException:
        company = 'nan'
        
    try:
        location = details.find_element_by_css_selector(
                'h4.pv-entity__location').get_attribute('innerText')
        location = location.split('\n', 1)[1]
    except NoSuchElementException:
        location = 'nan'
        
    try:
        dates = details.find_element_by_css_selector(
                "h4.pv-entity__date-range").get_attribute('innerText').split(' ', 2)[-1]
    except NoSuchElementException:
            dates = 'nan'
    
    df = pd.DataFrame()
    df['job1'] = pos
    df['company1'] = company
    df['location1'] = location
    df['dates1'] = date_list
    df['first_name'] = fname_list
    df['email'] = email_list
    job_list.append(pos)
    company_list.append(company)
    date_list.append(dates)
    location_list.append(location)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    
    time.sleep(2)


# In[9]:


def get_email():
    # scroll to top of profile where email is located
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    contact_info = driver.find_element_by_css_selector(
        'a[data-control-name="contact_see_more"]')
     # js function to click banner/button to see additional results under jobs, people, or posts                      
    driver.execute_script('arguments[0].click();',contact_info)
    time.sleep(3)
    try:
        container =  driver.find_elements_by_css_selector(
            'div.pv-contact-info__ci-container')
        email =  container[1].get_attribute('innerText')
     
    
    except (NoSuchElementException, IndexError):
        email = 'nan'
    
    email_list.append(email)
    close_popup = driver.find_element_by_css_selector(
            'button[aria-label="Dismiss" ]')
    close_popup.click()


# In[10]:


def profile_connect(message):
    # scroll to top of profile to ensure elements can be found by webdriver
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(5)
    # locate & click 'Connect' button located at top of profile
    driver.find_element_by_class_name('pv-s-profile-actions--connect').click()
    action_bar = driver.find_element_by_css_selector("div.artdeco-modal__actionbar")
    # locate 'Add a note' button by class
    action_bar.find_element_by_class_name('mr1').click()
    time.sleep(3)
    # action to send text from message to input box
    message_input = driver.find_element_by_id('custom-message').send_keys(message)
    # send the message & connection request
    driver.find_element_by_class_name('ml1').click()


# In[43]:


def profile_scrape(list_profile_urls):
    for url in list_profile_urls:
        driver.get(url)
        get_experience()
        #get_education()
        get_email()
    df = pd.DataFrame()
    df['profile_name'] = names_list
    df['job1'] = job_list
    df['company1'] = company_list
    df['location1'] = location_list
    df['dates1'] = date_list
    df['first_name'] = fname_list
    df['email'] = email_list
    return df

def make_connection(url_message_dict):
    counter = 1

    for key, value in url_message_dict.items():
        url = key
        message = value
        driver.get(url)
        profile_connect(message)
        print('connection to :  ' +url+ ' is complete')
        counter+=1
    print('Process complete '+str(counter)+ ' connections requested')


# In[13]:


PATH = "C:\Program Files (x86)\chromedriver.exe"


# In[14]:


driver = sign_in('email@gmail.com', 'password1!', PATH)


# In[44]:


def search_scrape_connect(search_term, num_pages):
    search_df = people_scrape(search_term, num_pages)

    profile_urls = search_df['fetch']

    detail_df = profile_scrape(profile_urls)

    df = pd.concat([search_df, detail_df], axis=1)
    df = df.loc[df.company1 != 'nan']
    df = df.loc[df.job1 != 'nan']
    df['first_name'] = df.name.apply(lambda x: (x.split(' ', 1)[0]))
    df['personalized_message'] = ("Hi " + df.first_name +", my name is Brennan, and I am a data scientist in the DMV area."
                                                       "My background is in video editing but after completing several courses, I am transitioning into the "
                                                       " ds career field, hoping to segue into AI. I see that you are a " + df.job1 + "at "+ df.company1+
                                                       ", which sounds super interesting, so I just wanted to reach out, connect, and say hello!")  
    message_inputs = list(df['personalized_message'])
    urls = list(df['fetch'])
    connection_dict = dict(zip(urls, message_inputs))
    df.to_csv(search_term+'_comp.csv')
    make_connection(connection_dict)
    return df
    driver.quit()


# In[42]:


location_list = []
current_job_list = []
name_list = []
url_list = []
headline_list = []
names_list = []
email_list = []
job_list = []
company_list = []
loc_list = []
date_list = []
search_scrape_connect('machine learning engineer', 3)

