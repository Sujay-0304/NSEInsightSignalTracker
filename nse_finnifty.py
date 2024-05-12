# import requests
# import pandas as pd
# import time
# import httpx 

# url = 'https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY'
# # header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37','accept-encoding': 'gzip, deflate, br','accept-language': 'en-GB,en;q=0.9,en-US;q=0.8'}

# header = {
#     'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
#     'accept-encoding': 'gzip, deflate, br, zstd',
#     'accept-language': 'en-US,en;q=0.9',
   

# }
# session = requests.Session()
# request = session.get(url,headers=header)
# # cookies = dict(request.cookies)
# print(request.status_code) 

from selenium import webdriver
import pandas as pd
import time

url = 'https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY'
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # To run Chrome in headless mode
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-dev-shm-usage') # Overcome limited resource problems

# Path to your ChromeDriver executable
driver_path = 'C:/Users/HP/Downloads/chromedriver_win32/chromedriver.exe'

def fetch_data_with_selenium():
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to render the data
    data = driver.find_element_by_tag_name('pre').text  # Extract the text from <pre> tag
    driver.quit()
    return data

data = fetch_data_with_selenium()
print(data)


