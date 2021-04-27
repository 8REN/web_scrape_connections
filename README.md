# web_scrape_connections
* the goal here is to search linkedin for connections, jobs, location based profiles, from search response, create dataframe with url and name of person with other details visible in minimized search format, then to iterate through urls and scrape the info from each profile, creating another csv, with all info, and create personalized message with which i can use to connect with user.

### instructions on installing driver on chrome found

https://datainsights.data.blog/2021/01/17/web-scraping-with-selenium/

 
can be used with other browsers, safari, opera, explorer, firefox, etc. must have matching driver for browser
selenium:
*automate login 
*navigate page buttons and pagination
*initial data scrape from search results to obtain name and url of profile
*iterate through urls 
*scrape individual profile for 
*** name
*** employment
*** education
*** email
*** use these columns to create a string in a new column for message to send upon requesting to 'connect' 

# tools required to run 
### must install selenium (pip install selenium)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import csv
import numpy as np
import pandas as pd
import requests
import re

Once driver is initialized, expand Selenium controlled browser window to full screen.
For best results, set browser font in window opened by selenium to 'extra small' and expand window.
Make sure that 'inspect' window is as small as possible due to dynamic loading nature of ajax format webpage.
Otherwise, some elements will not be found by webdriver, throwing error causing script to stop running.

Can only do web scraping on full profile, getting experience and education information on 100 profiles or so at once, max.
Website will not handle more than this. Can get several pages of search results archived at once, then slice profile urls list