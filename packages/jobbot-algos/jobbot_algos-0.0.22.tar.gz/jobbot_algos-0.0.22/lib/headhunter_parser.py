#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import fastcore.basics as fcb
from time import sleep
from random import uniform
import re
from jobbot_algos.postgres import PostgresConnector
from tqdm import tqdm
from jobbot_algos.core import logger
from jobbot_algos.driver import Driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# In[ ]:





# # Base:

# In[2]:


class Base:
    
    def __init__(self, ssh_username:str, ssh_password:str, postgres_username:str, postgres_password:str):
        
        postgres_creds = {'ssh_host':'185.247.17.122',
                          'ssh_username':ssh_username,
                          'ssh_password':ssh_password,
                          'local_host':'localhost',
                          'postgres_username':postgres_username,
                          'postgres_password':postgres_password,
                          'database':'jobbot_db'
                         }
                
        self.pc = PostgresConnector(**postgres_creds)


# # сlass HeadHunterParser:

# In[3]:


class HeadHunterParser(Base):
    base_url = 'https://api.hh.ru/vacancies'

    def __init__(self, ssh_username:str, ssh_password:str, postgres_username:str, postgres_password:str):
        super().__init__(ssh_username, ssh_password, postgres_username, postgres_password)


# ### run:

# In[4]:


@fcb.patch_to(HeadHunterParser)

def run(self, professional_role:int, area:int, save_to_postgres=False) -> pd.DataFrame:
    
    # 1. GET URLS:
    urls = []
    for page in tqdm(range(20), desc='Pages'):
        
        params = {'professional_role':professional_role, 'area':area, 'per_page':100, 'page':page} 
        json = requests.get(self.base_url, params=params).json()
        
        # break if pages are over:
        if len(json['items'])==0: break
        
        urls += pd.Series(json['items']).apply(lambda x: x['url']).to_list()
        
        # sleep:
        sleep(uniform(3,5))
        
    # 2. GET VACANCIES' INFO:
    dfs = []
    for url in tqdm(urls, desc='URLs'):

        json = requests.get(url).json()

        df = pd.DataFrame({'id':[json['id']], 
                           'name':[json['name']], 
                           'profession':[json['professional_roles'][0]['name']],
                           'salary':[json['salary']], 
                           'key_skills':[json['key_skills']], 
                           'experience':[json['experience']], 
                           'description':[json['description']], 
                           'schedule':[json['schedule']],
                           'company':json['employer']['name']})

        dfs.append(df)
        sleep(uniform(1,3))

    data = pd.concat(dfs)
    data['description'] = data['description'].apply(lambda x: re.sub(re.compile('<.*?>'), '', x))
    data['key_skills']  = data['key_skills'].apply(lambda x: ', '.join([d['name'] for d in x]))
    data['experience']  = data['experience'].apply(lambda x: x['name'])
    data['schedule']    = data['schedule'].apply(lambda x: x['id'])
    data['salary_from'] = data['salary'].apply(lambda x: x['from'] if type(x)==dict else None)
    data['salary_to']   = data['salary'].apply(lambda x: x['to'] if type(x)==dict else None)
    data['currency']    = data['salary'].apply(lambda x: x['currency'] if type(x)==dict else None)
    data['area'] = area
    data = data[['id', 'area', 'profession', 'name', 'company', 'key_skills', 'experience', 'description', 'schedule', 'salary_from', 'salary_to', 'currency']]
    
    if save_to_postgres:
        self.pc.save(df=data, table_name='hh_vacancies', schema='main_schema', if_table_exists="append")
        
    return data


# # class GetMatchParser:

# In[5]:


class GetMatchParser(Base):
    base_url = 'https://getmatch.ru/vacancies?p={}&pa=all'

    def __init__(self, ssh_username:str, ssh_password:str, postgres_username:str, postgres_password:str):
        super().__init__(ssh_username, ssh_password, postgres_username, postgres_password)
        
        # get driver:
        self.driver = Driver(headless=True).get_driver()


# ### get_df:

# In[6]:


@fcb.patch_to(GetMatchParser)

def get_df(self, url: str) -> pd.DataFrame:
    
    """
    МЕТОД ДЛЯ ПОЛУЧЕНИЯ pd.DataFrame ВАКАНСИИ ПО ЕЕ ССЫЛКЕ на getmatch
    
    Parameters:
    url: str - ссылка (напр: https://getmatch.ru/vacancies/16428-razrabotchik-bekenda-poisk?s=offers)
    
    Returns:
    pd.DataFrame
    """
    
    self.driver.get(url)
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'b-header'))) 
    pageSource = self.driver.page_source
    bs = BeautifulSoup(pageSource, 'html.parser')
    
    # name:
    try: name = bs.find('h1', {'_ngcontent-serverapp-c89': ''}).get_text()
    except: name = None
    
    # company:
    try: company = bs.find('h2', {'_ngcontent-serverapp-c89': ''}).get_text().replace('в\xa0', '')
    except: company = None
    
    # salary:
    try: salary = bs.find('h3', {'_ngcontent-serverapp-c89': ''}).get_text().strip()
    except: salary = None
    
    # profession:
    try: profession = bs.findAll('div', {'class':'col b-value'})[0].get_text()
    except: profession = None
    
    # grade:
    try: grade = bs.findAll('div', {'class':'col b-value'})[1].get_text()
    except: grade = None
    
    # skills:
    try:
        elems = bs.find('div', {'class':'b-vacancy-stack-container'}).findAll('span', {'class':'g-label'})
        skills = ', '.join([elem.get_text() for elem in elems])
    except:
        skills = None
        
    # description:
    try:
        description = bs.find('section', {'class':'b-vacancy-description markdown'}).get_text().strip().replace('\n', ' ')
    except:
        description = None
        
    # locations:
    try:
        main_location = bs.find('span', {'class':'g-label g-label-secondary b-vacancy-locations--first'}).get_text()
        secondary_elems = bs.findAll('span', {'class':'g-label g-label-secondary'})
        secondary_location = ', '.join([elem.get_text() for elem in secondary_elems])
        locations = f'{main_location}, {secondary_location}'
    except:
        locations = None
        
    # schedule:
    try:
        elems = bs.findAll('span', {'class':'g-label g-label-zanah'})
        schedule = ', '.join([elem.get_text() for elem in elems])
    except:
        schedule = None
        
                
    return pd.DataFrame({'url':[url], 'locations':[locations], 'profession':[profession], 'name':[name], 'company':[company], 
                         'skills':[skills], 'grade':[grade], 'description':[description], 'schedule':[schedule], 'salary':[salary]})


# ### run:

# In[7]:


@fcb.patch_to(GetMatchParser)

def run(self) -> pd.DataFrame:
    
    # 1. URLS:
    page = 1
    urls = []
    while True:
        self.driver.get(self.base_url.format(page))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'b-vacancies-list__count'))) 
        pageSource = self.driver.page_source
        bs = BeautifulSoup(pageSource, 'html.parser')

        if len(bs.findAll('div',{'class':'b-vacancy-card'}))==0: break

        for element in bs.findAll('div',{'class':'b-vacancy-card'}):
            href = element.find('a', {'target':'_blank'}).get('href')
            url = f'https://getmatch.ru{href}'
            urls.append(url)

        page += 1
        
        
    # 2. GET VACANCIES' INFO:
    dfs = []
    for url in tqdm(urls, desc='URLs'):
        df = self.get_df(url)
        dfs.append(df)
    
    self.driver.close()
        
    return pd.concat(dfs)


# In[8]:


# creds = {'ssh_username':'root', 'ssh_password':'aRGgMeM7wBQ2m*', 'postgres_username':'jobbot', 'postgres_password':'12345',}
# g = GetMatchParser(**creds)
# getmatch_data = g.run()
# getmatch_data['is_remote'] = (getmatch_data.schedule.str.contains('удал')).astype(int)


# In[ ]:





# In[9]:


# driver = Driver(headless=False).get_driver()
# dfs = []
# for url in tqdm(urls[11::]):
#     driver.get(url)
#     sleep(0.2)
#     pageSource = driver.page_source
#     bs = BeautifulSoup(pageSource, 'html.parser')
    
#     name       = bs.find('h1', {'_ngcontent-serverapp-c89': ''}).get_text()
#     company    = bs.find('h2', {'_ngcontent-serverapp-c89': ''}).get_text().replace('в\xa0', '')
#     salary     = bs.find('h3', {'_ngcontent-serverapp-c89': ''}).get_text().strip()
#     profession = bs.findAll('div', {'class':'col b-value'})[0].get_text()
#     grade      = bs.findAll('div', {'class':'col b-value'})[1].get_text()

#     # skills:
#     elems = bs.find('div', {'class':'b-vacancy-stack-container'}).findAll('span', {'class':'g-label'})
#     skills = ', '.join([elem.get_text() for elem in elems])

#     # description:
#     description = bs.find('section', {'class':'b-vacancy-description markdown'}).get_text().strip().replace('\n', ' ')

#     # locations:
#     main_location = bs.find('span', {'class':'g-label g-label-secondary b-vacancy-locations--first'}).get_text()
#     secondary_elems = bs.findAll('span', {'class':'g-label g-label-secondary'})
#     secondary_location = ', '.join([elem.get_text() for elem in secondary_elems])
#     locations = f'{main_location}, {secondary_location}'

#     # schedule:
#     elems = bs.findAll('span', {'class':'g-label g-label-zanah'})
#     schedule = ', '.join([elem.get_text() for elem in elems])

#     df = pd.DataFrame({'url':[url], 'locations':[locations], 'profession':[profession], 'name':[name], 'company':[company], 
#                            'skills':[skills], 'grade':[grade], 'description':[description], 'schedule':[schedule], 'salary':[salary]})

#     dfs.append(df)


# In[10]:


# name       = bs.find('h1', {'_ngcontent-serverapp-c89': ''}).get_text()
# company    = bs.find('h2', {'_ngcontent-serverapp-c89': ''}).get_text().replace('в\xa0', '')
# salary     = bs.find('h3', {'_ngcontent-serverapp-c89': ''}).get_text().strip()
# profession = bs.findAll('div', {'class':'col b-value'})[0].get_text()
# grade      = bs.findAll('div', {'class':'col b-value'})[1].get_text()

# # skills:
# elems = bs.find('div', {'class':'b-vacancy-stack-container'}).findAll('span', {'class':'g-label'})
# skills = ', '.join([elem.get_text() for elem in elems])

# # description:
# description = bs.find('section', {'class':'b-vacancy-description markdown'}).get_text().strip().replace('\n', ' ')

# # locations:
# main_location = bs.find('span', {'class':'g-label g-label-secondary b-vacancy-locations--first'}).get_text()
# secondary_elems = bs.findAll('span', {'class':'g-label g-label-secondary'})
# secondary_location = ', '.join([elem.get_text() for elem in secondary_elems])
# locations = f'{main_location}, {secondary_location}'

# # schedule:
# elems = bs.findAll('span', {'class':'g-label g-label-zanah'})
# schedule = ', '.join([elem.get_text() for elem in elems])

# df = pd.DataFrame({'url':[url], 'locations':[locations], 'profession':[profession], 'name':[name], 'company':[company], 'skills':[skills], 'grade':[grade], 'description':[description], 'schedule':[schedule], 'salary':[salary]})


# In[11]:


# %%time
# hh = HeadHunterParser()
# data = hh.run(professional_role=165, area=1)
# pc.execute(f"DELETE FROM main_schema.hh_vacancies WHERE area = {data['area'].values[0]} AND profession = '{data['profession'].values[0]}'")
# pc.save(df=data, table_name='hh_vacancies', schema='main_schema', if_table_exists="append")


# In[12]:


# postgres_creds = {'ssh_host':'185.247.17.122',
#                   'ssh_username':'root',
#                   'ssh_password':'aRGgMeM7wBQ2m*',
#                   'local_host':'localhost',
#                   'postgres_username':'jobbot',
#                   'postgres_password':'12345',
#                   'database':'jobbot_db'
#                  }


# In[13]:


# pc = PostgresConnector(**postgres_creds)
# pc.check_connection()


# In[14]:


# creds = {'ssh_username':'root', 'ssh_password':'aRGgMeM7wBQ2m*', 'postgres_username':'jobbot', 'postgres_password':'12345',}

# hh = HeadHunterParser(**creds)


# In[15]:


# %%time
# data = hh.run(professional_role=121, area=2, save_to_postgres=False)


# In[16]:


# pc = PostgresConnector(**postgres_creds)


# In[17]:


# %%time
# df = pc.download('select * from main_schema.hh_vacancies')


# In[ ]:




