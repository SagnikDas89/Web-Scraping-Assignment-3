#!/usr/bin/env python
# coding: utf-8

# 1

# In[1]:


# lets first install the selinium library
get_ipython().system(' pip install selenium')


# In[2]:


# lets now import all the required libraries
from bs4 import BeautifulSoup
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
import csv
import io
import hashlib
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException           # Importing Exceptions
#Importing requests
import requests
# importing regex
import re


# In[3]:


# Lets first connect to the web driver
driver = webdriver.Chrome("chromedriver.exe") 


# In[4]:


url = 'https://www.amazon.in/'
driver.get(url)


# In[5]:


search_guitars = driver.find_element_by_id('twotabsearchtextbox')
search_guitars


# In[6]:


# write on search bar
search_guitars.send_keys("Guitars")


# In[7]:


# do click using class_name function
search_btn = driver.find_element_by_class_name('nav-search-submit-text')
search_btn.click()


# In[ ]:





# In[ ]:


2


# In[ ]:


#open 'amazonguiter.csv' file in write mode
csv_file = open('amazonguiter.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)


# In[8]:


# so lets extract all the tags having the Guiter-titles, Brands, Ratings, Name_of_the_product, Price of_page_1
titles_tags=driver.find_elements_by_xpath("//div[@class='a-section a-spacing-none']")
titles_tags


# In[9]:


# Now the text of the guitar title, Brands, Ratings, Name_of_the_product, Price of_page_1 is inside the tags extracted above of page 1

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
guitar_titles=[]
for i in titles_tags:
    guitar_titles.append(i.text)
guitar_titles 


# In[12]:


# so lets extract all the tags having the Guiter-titles, Brands, Ratings, Name_of_the_product, Price of_page_2
titles_tags=driver.find_elements_by_xpath("//div[@class='a-section a-spacing-none']")
titles_tags


# In[13]:


# Now the text of the guitar title, Brands, Ratings, Name_of_the_product, Price of_page_2 is inside the tags extracted above of page 2

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
guitar_titles=[]
for i in titles_tags:
    guitar_titles.append(i.text)
guitar_titles 


# In[14]:


# so lets extract all the tags having the Guiter-titles, Brands, Ratings, Name_of_the_product, Price of_page_3
titles_tags=driver.find_elements_by_xpath("//div[@class='a-section a-spacing-none']")
titles_tags


# In[15]:


# Now the text of the guitar title, Brands, Ratings, Name_of_the_product, Price of_page_3 is inside the tags extracted above of page 2

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
guitar_titles=[]
for i in titles_tags:
    guitar_titles.append(i.text)
guitar_titles 


# In[ ]:





# In[ ]:


3


# In[17]:


import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib

# All in same directory
DRIVER_PATH = 'chromedriver.exe'


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)        
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    error_clicks = 0
    while (image_count < max_links_to_fetch) & (error_clicks < 30): # error clicks to stop when there are no more results to show by Google Images. You can tune the number
        scroll_to_end(wd)

        print('Starting search for Images')

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:max_links_to_fetch]:
            # try to click every thumbnail such that we can get the real image behind it
            print("Total Errors till now:", error_clicks)
            try:
                print('Trying to Click the Image')
                img.click()
                time.sleep(sleep_between_interactions)
                print('Image Click Successful!')
            except Exception:
                error_clicks = error_clicks + 1
                print('ERROR: Unable to Click the Image')
                if(results_start < number_results):
                	continue
                else:
                	break
                	
            results_start = results_start + 1

            # extract image urls    
            print('Extracting of Image URLs')
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            print('Current Total Image Count:', image_count)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
            else:
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")
            	        
        results_start = len(thumbnail_results)

    return image_urls

def persist_image(folder_path:str,file_name:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

if __name__ == '__main__':
    wd = webdriver.Chrome(executable_path=DRIVER_PATH)
    queries = ["Fruits", "Cars", 'Machine_Learning']  #change your set of queries here
    for query in queries:
        wd.get('https://google.com')
        search_box = wd.find_element_by_css_selector('input.gLFyf')
        search_box.send_keys(query)
        links = fetch_image_urls(query,100,wd) # 100 denotes no. of images you want to download
        images_path = 'dataset/'
        for i in links:
            persist_image(images_path,query,i)
    wd.quit()


# In[ ]:





# In[ ]:


4


# In[18]:


driver=webdriver.Chrome("chromedriver.exe") 
time.sleep(3)

url = "https://www.flipkart.com/"
driver.get(url)

time.sleep(2)
#locating the search bar
search_bar=driver.find_element_by_class_name("_3704LK")
search_bar.send_keys('smartphones')

time.sleep(2)
#locating the button and clicking it toh search for sunglasses
button=driver.find_element_by_class_name('L0Z3Pu')
button.click()


# In[ ]:


# name of csv file 
filename = "smartphones.csv"
    
# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerows(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)


# In[20]:


#creating the empty list
brand_name=[]
smartphone_name=[]
color=[]
ram=[]
rom=[]
primary_camera=[]
secondary_camera=[]
display_size=[]
display_resolution=[]
processor=[]
processor_cores=[]
battery_capacity=[]
description=[]
price=[]


# In[21]:


time.sleep(3)
#scrapping the required details
start=0
end=3


# In[22]:


# so lets extract all the tags having the brand-titles, smartphone_names, color
titles_tags=driver.find_elements_by_xpath("//div[@class='_4rR01T']")
titles_tags


# In[23]:


# Now the text of the brand title, smartphone_names, color are inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
brand_titles=[]
for i in titles_tags:
    brand_titles.append(i.text)
brand_titles 


# In[24]:


# so lets extract all the tags having the titles RAM, ROM, Display_size, Display_resolution, Primary_camera, Secondary_camera, Battery_capacity, Processor, Price, Description
titles_tags=driver.find_elements_by_xpath("//li[@class='rgWa7D']")
titles_tags


# In[25]:


# Now the text of the RAM, ROM, Display_size, Display_resolution, Primary_camera, Secondary_camera, Battery_capacity, Processor, Price, Description title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
ram_titles=[]
for i in titles_tags:
    ram_titles.append(i.text)
ram_titles


# In[ ]:


#creating a dataframe
df=pd.DataFrame({'Brand':brand,
                'Description':description,
                'Price':price,
                'RAM':ram,
                'ROM':rom,
                'Battery':battery,
                'Primary_Camera':primary_camera,
                'Secondary_Camera':secondary_camera,
                'Display':display,
                'Processor':processor})
#printing dataframe
df


# In[ ]:


#closing csv file
csv_file.close()

#closing driver
driver.close()


# In[ ]:





# In[ ]:


5


# In[26]:


import pandas as pd 
import numpy as np
    



from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

# Define a dictionary containing  data 
data = {'City':['Bangalore', 'Mumbai', 'Chennai', 'Delhi', 'Kolkata']} 
    
# Convert the dictionary into DataFrame 
df = pd.DataFrame(data) 
    
# Observe the result 
df 
   
# declare an empty list to store
# latitude and longitude of values 
# of city column
longitude = []
latitude = []
   
# function to find the coordinate
# of a given city 
def findGeocode(city):
       
    # try and catch is used to overcome
    # the exception thrown by geolocator
    # using geocodertimedout  
    try:
          
        # Specify the user_agent as your
        # app name it should not be none
        geolocator = Nominatim(user_agent="your_app_name")
          
        return geolocator.geocode(city)
      
    except GeocoderTimedOut:
          
        return findGeocode(city)    
  
# each value from city column
# will be fetched and sent to
# function find_geocode   
for i in (df["City"]):
      
    if findGeocode(i) != None:
           
        loc = findGeocode(i)
          
        # coordinates returned from 
        # function is stored into
        # two separate list
        latitude.append(loc.latitude)
        longitude.append(loc.longitude)
       
    # if coordinate for a city not
    # found, insert "NaN" indicating 
    # missing value 
    else:
        latitude.append(np.nan)
        longitude.append(np.nan)
# now add this column to dataframe
df["Longitude"] = longitude
df["Latitude"] = latitude
df


# In[ ]:





# In[ ]:


6


# In[3]:


# Lets first connect to the web driver
driver = webdriver.Chrome("chromedriver.exe") 

url = 'https://trak.in/india-startup-funding-investment-2015/'
driver.get(url)


# In[4]:


# so lets extract all the tags having the month-titles
titles_tags=driver.find_elements_by_xpath("//h2[@class='tablepress-table-name tablepress-table-name-id-48']")
titles_tags


# In[5]:


# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
month_titles=[]
for i in titles_tags:
    month_titles.append(i.text)
month_titles 


# In[6]:


# so lets extract all the tags having the month-titles
titles_tags=driver.find_elements_by_xpath("//h2[@class='tablepress-table-name tablepress-table-name-id-49']")
titles_tags


# In[7]:


# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
month_titles=[]
for i in titles_tags:
    month_titles.append(i.text)
month_titles 


# In[8]:


# so lets extract all the tags having the month-titles
titles_tags=driver.find_elements_by_xpath("//h2[@class='tablepress-table-name tablepress-table-name-id-50']")
titles_tags


# In[9]:


# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
month_titles=[]
for i in titles_tags:
    month_titles.append(i.text)
month_titles 


# In[10]:


# so lets extract all the tags having the month-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='dataTables_scroll']/div")
titles_tags


# In[11]:


# so lets extract all the tags having the month-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='dataTables_scroll']/div/div/div")
titles_tags


# In[ ]:





# In[ ]:


7


# In[13]:


# lets first install the selinium library
get_ipython().system(' pip install selenium')


# In[14]:


# lets now import all the required libraries
import selenium
import pandas as pd
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException           # Importing Exceptions


# In[15]:


# Lets first connect to the web driver
driver = webdriver.Chrome("chromedriver.exe") 

url = 'https://www.digit.in/top-products/best-gaming-laptops-40.html'
driver.get(url)


# In[16]:


# so lets extract all the tags having the gaming laptop-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='Top10-Seller']")
titles_tags


# In[17]:


# Now the text of the gaming laptop title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
laptop_titles=[]
for i in titles_tags:
    laptop_titles.append(i.text)
laptop_titles 


# In[ ]:





# In[ ]:


8


# In[18]:


# lets first install the selinium library
get_ipython().system(' pip install selenium')


# In[19]:


#import selenium package
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import re


# In[20]:


# Lets first connect to the web driver
driver = webdriver.Chrome("chromedriver.exe") 
driver.get("https://www.forbes.com/billionaires/list/50/#version:static")

#open 'billionaires.csv' file in write mode
csv_file = open('billionaires.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)


# In[21]:


# so lets extract all the tags having the billionaires-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='personName']")
titles_tags


# In[22]:


# Now the text of the name title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
name_titles=[]
for i in titles_tags:
    name_titles.append(i.text)
name_titles 


# In[23]:


# so lets extract all the tags having the worth-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='netWorth']")
titles_tags


# In[24]:


# Now the text of the worth title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
worth_titles=[]
for i in titles_tags:
    worth_titles.append(i.text)
worth_titles 


# In[25]:


# so lets extract all the tags having the worth-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='rank']")
titles_tags


# In[26]:


# Now the text of the rank title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
rank_titles=[]
for i in titles_tags:
    rank_titles.append(i.text)
rank_titles 


# In[27]:


# so lets extract all the tags having the country-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='countryOfCitizenship']")
titles_tags


# In[28]:


# Now the text of the country title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
country_titles=[]
for i in titles_tags:
    country_titles.append(i.text)
country_titles 


# In[29]:


# so lets extract all the tags having the age-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='age']")
titles_tags


# In[30]:


# Now the text of the age title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
age_titles=[]
for i in titles_tags:
    age_titles.append(i.text)
age_titles


# In[31]:


# so lets extract all the tags having the source-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='source-column']")
titles_tags


# In[32]:


# Now the text of the source title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
source_titles=[]
for i in titles_tags:
    source_titles.append(i.text)
source_titles


# In[33]:


# so lets extract all the tags having the industry-titles
titles_tags=driver.find_elements_by_xpath("//div[@class='category']")
titles_tags


# In[34]:


# Now the text of the industry title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
industry_titles=[]
for i in titles_tags:
     industry_titles.append(i.text)
industry_titles


# In[ ]:


# writing to csv file 
with open(csv_file, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)


# In[37]:


#closing csv file
csv_file.close()

#closing driver
driver.close()


# In[ ]:





# In[ ]:


9


# In[ ]:


from selenium import webdriver
import time
import os
import csv
import pandas as pd
from math import ceil

# Creates a new .csv file that the data will be written to

csv_file = open('c:\\Documents\\output_scraping.csv', 'w', encoding="UTF-8", newline="")
writer = csv.writer(csv_file)

# write header names
writer.writerow(
    ['url', 'link_title', 'channel', 'no_of_views', 'time_uploaded', 'comment', 'author', 'comment_posted', 
     'no_of_replies','upvotes','downvotes'])

# open chrome 
youtube_pages = "https://www.youtube.com/"
driver = webdriver.Chrome
driver.get(youtube_pages)
time.sleep(10)
try:
    print("=" * 500)  # Shows in terminal when youtube summary page with search keyword is being scraped
    print("Scraping " + youtube_pages)
    search = driver.find_element_by_id('search')
    search.send_keys("Data Science")    
    driver.find_element_by_id('search-icon-legacy').click()
    time.sleep(20)    
    vtitle = driver.find_elements_by_id('video-title')
    subscription = driver.find_elements_by_id('byline')
    views = driver.find_elements_by_xpath('//div[@id="metadata-line"]/span[1]')
    posted = driver.find_elements_by_xpath('//div[@id="metadata-line"]/span[2]')
    
    tcount = 0
    href = []
    title = []
    channel = []
    numview = []
    postdate = []
        
    while tcount < 10:
        href.append(vtitle[tcount].get_attribute('href'))
        channel.append(subscription[tcount].get_attribute('title'))
        title.append(vtitle[tcount].text)
        numview.append(views[tcount].text)
        postdate.append(posted[tcount].text)  
        tcount = tcount +1
    
    # launch top ten extracted links and extract comment details
    tcount = 0    
    while tcount < 10:  
        youtube_dict ={}
        # extract comment section of top ten links
        url = href[tcount]
        print (url)
        driver.get(url)
        time.sleep(5)
        
        try:
            print("+" * 40)  # Shows in terminal when details of a new video is being scraped
            print("Scraping child links ")
            #scroll down to load comments
            driver.execute_script('window.scrollTo(0,500);')
            time.sleep(15)
            #sort by top comments
            sort= driver.find_element_by_xpath("""//*[@id="icon-label"]""")
            sort.click()
            time.sleep(10)
            topcomments =driver.find_element_by_xpath("""//*[@id="menu"]/a[1]/paper-item/paper-item-body/div[1]""")
            topcomments.click()
            time.sleep(10)
            # Loads 20 comments , scroll two times to load next set of 40 comments. 
            for i in range(0,2):
                driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight))")
                time.sleep(10)
            
            #count total number of comments and set index to number of comments if less than 50 otherwise set as 50. 
            totalcomments= len(driver.find_elements_by_xpath("""//*[@id="content-text"]"""))
         
            if totalcomments < 50:
                index= totalcomments
            else:
                index= 50 
                
            ccount = 0
            while ccount < index: 
                try:
                    comment = driver.find_elements_by_xpath('//*[@id="content-text"]')[ccount].text
                except:
                    comment = ""
                try:
                    authors = driver.find_elements_by_xpath('//a[@id="author-text"]/span')[ccount].text
                except:
                    authors = ""
                try:
                    comment_posted = driver.find_elements_by_xpath('//*[@id="published-time-text"]/a')[ccount].text
                except:
                    comment_posted = ""
                try:
                    replies = driver.find_elements_by_xpath('//*[@id="more-text"]')[ccount].text                    
                    if replies =="View reply":
                        replies= 1
                    else:
                        replies =replies.replace("View ","")
                        replies =replies.replace(" replies","")
                except:
                    replies = ""
                try:
                    upvotes = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')[ccount].text
                except:
                    upvotes = ""
                        
                youtube_dict['url'] = href[tcount]
                youtube_dict['link_title'] = title[tcount]
                youtube_dict['channel'] = channel[tcount]
                youtube_dict['no_of_views'] = numview[tcount]
                youtube_dict['time_uploaded'] =  postdate[tcount]
                youtube_dict['comment'] = comment
                youtube_dict['author'] = authors
                youtube_dict['comment_posted'] = comment_posted
                youtube_dict['no_of_replies'] = replies
                youtube_dict['upvotes'] = upvotes
                
                writer.writerow(youtube_dict.values())
                ccount = ccount +1
                
        except Exception as e:
            print(e)
            driver.close()
        tcount = tcount +1 
    print("Scrapping process Completed")   
    csv_file.close()    
except Exception as e:
    print(e)
    driver.close()


# In[ ]:





# In[ ]:


10


# In[57]:


# lets first install the selinium library
get_ipython().system(' pip install selenium')


# In[58]:


# lets now import all the required libraries
import selenium
import pandas as pd
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException           # Importing Exceptions


# In[59]:


# Lets first connect to the web driver
driver = webdriver.Chrome("chromedriver.exe") 

url = 'https://www.hostelworld.com'
driver.get(url)


# In[61]:


search_locations = driver.find_element_by_id('search-input-field')
search_locations


# In[60]:


# finding element for hostels location bar
search_loc = driver.find_element_by_id("search-input-field")
search_loc.send_keys("London")


# In[63]:


# do click using class_name function
search_btn = driver.find_element_by_id('search-button')
search_btn.click()


# In[64]:


# so lets extract all the tags having the hostels-titles of page 1
hostels_tags=driver.find_elements_by_xpath("//h2[@class='title title-6']/a")
hostels_tags


# In[65]:


# Now the text of the hostels title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
hostels_titles=[]
for i in hostels_tags:
    hostels_titles.append(i.text)
hostels_titles 


# In[66]:


# so lets extract all the tags having the loctions-titles of page 1
locations_tags=driver.find_elements_by_xpath("//span[@class='description']")
locations_tags


# In[67]:


# Now the text of the locations title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
locations_titles=[]
for i in locations_tags:
    locations_titles.append(i.text)
locations_titles 


# In[68]:


# so lets extract all the tags having the ratings-titles 
ratings_tags=driver.find_elements_by_xpath("//div[@class='summary orange']")
ratings_tags


# In[69]:


# Now the text of the ratings, reviews title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
ratings_titles=[]
for i in ratings_tags:
    ratings_titles.append(i.text)
ratings_titles 


# In[70]:


# so lets extract all the tags having the dorms_titles 
dorms_tags=driver.find_elements_by_xpath("//div[@class='price title-5']")
ratings_tags


# In[ ]:


# Now the text of the dorms title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
dorms_titles=[]
for i in dorms_tags:
    dorms_titles.append(i.text)
dorms_titles


# In[ ]:


# so lets extract all the tags having the privates titles 
privates_tags=driver.find_elements_by_xpath("//div[@class='price-col']/p")
privates_tags


# In[ ]:


# Now the text of the privates title is inside the tags extracted above

# so we will run a loop to iterate over the tags extracted above and extract the text inside them.
privates_titles=[]
for i in privates_tags:
    privates_titles.append(i.text)
privates_titles


# In[ ]:


# scraping the full property-description, for scraping full job description we have to go in each of the properties separately
urls=[i.get_attribute("href")for i in driver.find_elements_by_xpath("//a[@class='content collapse-content']")]
for url in urls:
    try:
        
        driver.get(url)
        raw_description=driver.find_element_by_xpath("//section[@class='property-desc']/div[1]").text
        description=raw_description.replace("Contact Person","@@@@@")
        description= description.split("@@@@@")
        full_property_description.append(description[0])
    except NoSuchElementException :
        full_property_description.append("---")

