#!/usr/bin/env python
# coding: utf-8

# In[198]:


#This python code has been write and execute using google chrome 110.0.5481.100
#and the corresponding chromedriver.exe 


#We import all the necessary library
#In this work we will use selenium to scrap our unjobnet website


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm

#Package to send the the csv by email
import csv #
import smtplib # simply sent our email
from email.mime.text import MIMEText #  email libraries to add more 
from email.mime.multipart import MIMEMultipart
from  email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from os.path import basename
from  email.mime.application import MIMEApplication

#We set the path to the chromedriver.exe
PATH="C:/Users/GLC/Desktop/AIMS/REVIEW Course/BLOCK 4/Big Data Analysis/chromedriver.exe"

#We create a chrome webdrive interface which will be use later to open our website
driver=webdriver.Chrome(PATH)


# In[199]:


#We assign the url of our website
url='https://www.unjobnet.org/jobs/detail/'


# In[200]:


def Page_link(url_gine, url):
    '''
    Return the url of all the page of our research output
    url_gine is the base url containing the key words we want to search
    url is an empty list which will return as output
    we add the page number at the end of the link
    '''
    for j in range(1,20):
        url.append(url_gine+str(j))
    return url


# In[201]:


def Job_link(url):
    '''
    This function go true all the job on the page indexed by the parameter url and extract the job full description link
    url is a list containing of the web pages containing a list of job
    '''
    PATH="C:/Users/GLC/Desktop/AIMS/REVIEW Course/BLOCK 4/Big Data Analysis/chromedriver.exe"
    driver=webdriver.Chrome(PATH)
    from tqdm import tqdm
    List_link=[]
    #For each research pages, we extract the link of all job detail
    for j in tqdm(url):
        driver.get(j)
        for i in range(1,21):
            try:
                #We find and extract the link of each job in a given page
                List_link.append(driver.find_elements(By.CLASS_NAME, 'col-lg-12')[1]\
                    .find_elements(By.XPATH,'//*[@id="main"]/div[2]/div/div['+str(i)+']')[0]\
                    .find_elements(By.TAG_NAME, 'a')[1].get_property('href'))
            except:
                continue
    return List_link


# In[202]:


def job_data_extraction(List_link):
    '''
    For a given link of job this function extract all the needed information about the job
    when the desired value is not available it return an empty string
    To extract the information we use the function find_element by xpath
    
    list_link contain the list the link of all the job description
    '''
    
    from tqdm import tqdm
    List_link2=[]
    PATH="C:/Users/GLC/Desktop/AIMS/REVIEW Course/BLOCK 4/Big Data Analysis/chromedriver.exe"
    driver=webdriver.Chrome(PATH)
    for i in tqdm(List_link):
        driver.get(i)
        try:
            Position_title=driver.find_element(By.XPATH,'//*[@id="jheader"]/div/div[2]/div[1]').text
        except:
            Position_title=''
        try:
            organization_hiring=driver.find_element(By.XPATH,'//*[@id="jheader"]/div/div[2]/div[2]').text
        except:
            organization_hiring=''
        try:
            duty_station=driver.find_element(By.XPATH,'//*[@id="jheader"]/div/div[2]/div[4]').text
        except:
            duty_station=''
        try:
            position_status=driver.find_element(By.XPATH,'//*[@id="jheader"]/div/div[2]/span[2]/a').text
        except:
            position_status=''
        try:    
            date_posted=driver.find_element(By.XPATH,'//*[@id="jheader"]/div/div[3]/div[2]').text
        except:
            date_posted==''
        try:
            limit_date=driver.find_element(By.XPATH, '//*[@id="jheader"]/div/div[2]/div[6]/span').text
        except:
            limit_date=''
        job_description=i

        job={'Position_title':Position_title,'organization_hiring':organization_hiring,'duty_station':duty_station,'position_status':position_status,'date_posted':date_posted,'limit_date':limit_date,'job_description':job_description}
        List_link2.append(job)
        
    return List_link2


# In[203]:


#We create a list containing all the key words from which we want to search job
Key=['Data Scientist', 'Data Engineer', 'Data Analyst', 'Statistician', 'Research Officer']
key2=[]
for k in Key:
    key2.append(k.replace(' ','+'))


# In[204]:


#We call the Page_link function to get the link of all the result pages for the research of each key words
#We save the result in a list call Url
Url=[]
for k in key2:
    Url=Page_link('https://www.unjobnet.org/jobs/detail?keywords='+k+'&orderby=recent&page=', Url)


# In[205]:


#We call the function Job_link to get all the link to the job description using our research result pages Url

Link=Job_link(Url)

#We save these link in a csv file call Job_url.csv
df=pd.DataFrame(Link)
df.columns=['Job_link']
df.to_csv('job_url.csv', index=False)


# In[158]:


#We call the job_data_extraction function to extract all the job information 
#for each job for which we have the link to the description

List_link2=job_data_extraction(Link)

#We save these link in a csv file call New_job_data.csv
Data=pd.DataFrame(List_link2)
out_put='New_job_data.csv'
Data.to_csv(out_put, sep=',', index=False)


# In[196]:


pd.read_csv('New_job_data.csv')


# In[207]:


#Sending the job list by email

def email_send():
    mes=MIMEMultipart()
    mes["from"]="Samuel Samuel"
    mes["BCC"]=""
    #mes.attach("data.csv")
    mes["to"]="gisele.otiobo@aims-cameroon.org,zidanefoulefack@gmail.com,michaelkoungni@gmail.com,neilla.azongo@aims-cameroon.org,betelihemkebede57@gmail.com,christian.mbala@aims-cameroon.org,kamosamy8@gmail.com,samuel.taguieke@aims-cameroon.org"
    mes["subject"]="jobs_list"
    path='/home/samuel/AIMS_CAMEROON_2022_2023/Big _Data _Analytics _with _Python/Projcet'
    filename='New_job_data.csv'
    body=MIMEText('content','plain')
    with open(filename,'r') as file:
        attachment=MIMEApplication(file.read(),Name=basename(filename))
        attachment['Content-Disposition']='attachment;filename="{}"'.format(filename)
    mes.attach(attachment)
    with smtplib.SMTP(host='smtp.gmail.com',port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('samuel.taguieke@aims-cameroon.org','693581282Aims')
        smtp.send_message(mes)
        print("Sent...")


# In[ ]:


email_send()

