from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.remote.command import Command
# import undetected_chromedriver.v2 as uc
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd



product_id = "jumpshot"
product_id = input("Enter Product name = ")
product_url = f'https://www.myteemaze.com/{product_id}'




driver = None 
def initDriver():
    print("-> Initiating Driver")
    global driver 
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--headless')
    driver = webdriver.Firefox()  
    # driver = webdriver.Chrome(options=chrome_options)  
     
 
initDriver()

#cell 3
def makeSureDriverIsOpen():
    global driver
    try:
        driver.current_url
    except:
        initDriver()
makeSureDriverIsOpen()



driver.get(product_url)
time.sleep(5)

def pressESCKey():
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    
    try:
        close_btn = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.close.icon")))
        close_btn.click()
    except:
        pass
    
    
pressESCKey()
        
    
data_container = []
pressESCKey() 


product_tile_list = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ProductTileList div.ProductTile")))

 
for product_index,product in enumerate(product_tile_list[:]):
    # pressESCKey()
    print("-"*100)
    print("Current product index =  ", product_index+1, "| Remaining Products = ", len(product_tile_list)-product_index-1)
    product.click()
    # pressESCKey()
    # time.sleep(5)
    
    name_price =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-bdd='dropdown-container']"))).text.strip().split(" - $")
    product_name, product_price = name_price
    print("Product Name = ",product_name)
    print("Product Price = ",product_price)
        
    colors = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.color-tiles-container.seven-col div.bc-transparent.cursor-pointer.p-relative.br-full")))
    # pressESCKey()

    for color_index,color in enumerate(colors[:]):
        # pressESCKey()
        color.click() 
        # pressESCKey() 
        # time.sleep(5)
        
        
        
        color_name =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.RenderWhenVisible div.flex.items-center"))).text.replace("Color: ","")
        print("Current color = ", color_name, " | Remaing colors = ", len(colors)-color_index-1)
        
        current_image_url =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.RetailProductImage div.RetailImage  img")))
        current_image_url = current_image_url.get_attribute("src")
        print("Current Color Image URL = ", current_image_url)
        
        
        
        try:
            sizes =  WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#product_details_size_container div.fw-bold")))
        except: 
            # time.sleep(1)
            pressESCKey()   
            
            sizes =  WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#product_details_size_container div.fw-bold")))
            
        
        
         
        if len(sizes)>1:
            # pressESCKey()
            
            for size_index,size in enumerate(sizes):
                try:
                    size.click()
                except:   
                    pressESCKey()
                    size.click()
                # pressESCKey()
                current_price =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div span[data-bdd="price-information"] .color-red')))
                current_price = current_price.text 
                if(size.text != 'Size Guide'):
                    data_container.append(
                    [ 
                        product_name,color_name,current_price,size.text,current_image_url
                    ]
                ) 
                
                # data_container.append(
                #     [ 
                #         product_name,color_name,current_price,size.text,current_image_url
                #     ]
                # ) 
        else: 
            data_container.append(
                [
                    product_name,color_name,product_price,"N/A",current_image_url
                ]
            )  
        
        sizes = [x.text for x in sizes][1:] 
        print("Available Sizes = ", sizes)
        
    
    
df = pd.DataFrame(columns=["Product Type","Color Name","Price","Size","Image URL"], data=data_container )
df.to_csv("results.csv",index=False)  
        
    
     

# data_container

