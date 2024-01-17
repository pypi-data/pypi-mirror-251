#!/usr/bin/env python
# coding: utf-8

# In[8]:


from random import choice, uniform
from jobbot_algos.core import logger
import fastcore.basics as fcb
from bs4 import BeautifulSoup

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service


# # class Driver:

# In[9]:


class Driver:
    def __init__(self, executable_path='/usr/local/bin/chromedriver', headless=True):
        
        """
        Parameters:
        executable_path - путь до chromedriver
        headless - использовать ли интерфейс браузера (True - выключенный интерфейс)
        """
        
        # create executable_path:
        s = Service(executable_path=executable_path)
                
        # create options for the driver:
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
            
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        
        options.add_argument('--disable-infobars')
        
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-crash-reporter')
        options.add_argument('--disk-cache-size=0')
        options.add_argument('--disable-cache')
        
        # new:
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-application-cache")
        options.add_argument("--v8-cache-options=off")
        options.add_argument("--disable-offline-load-stale-cache")
        options.add_argument("--disable-back-forward-cache")
        
        # use random user-agent string:
        user_agent_strings = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
                              'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
                              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
                              'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36']
        
        random_user_agent = choice(user_agent_strings)
        options.add_argument(f"--user-agent={random_user_agent}")
        
        # start driver:
        self.driver = webdriver.Chrome(options=options, service=s)
                
        logger.info(f"SUCCESS: Chrome driver was created")


# ### get_driver:

# In[10]:


@fcb.patch_to(Driver)
def get_driver(self) -> selenium.webdriver.chrome.webdriver.WebDriver:
    
    """
    METHOD TO CREATE DRIVER.
    Return: selenium.webdriver
    """
    return self.driver


# In[11]:


# # EXAMPLE:
# driver = Driver(headless=True).get_driver() 


# In[ ]:




