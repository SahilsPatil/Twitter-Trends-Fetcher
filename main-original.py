from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from urllib.parse import quote
import time
import requests
import zipfile
from pymongo import MongoClient
from datetime import datetime
import uuid

MONGO_URI = "mongodb://localhost:27017/"  # Update for your MongoDB setup
DB_NAME = "twitter_trends"
COLLECTION_NAME = "trends"
X_USERNAME = "rohan249617897"
X_EMAIL = "abidan.daltyn@finestudio.org"
X_PASSWORD = "Rohan@1234"
PROXY_USERNAME = "abidann"
PROXY_PASSWORD = "abidann"
PROXY_HOST = "us-ca.proxymesh.com"
PROXY_PORT = "31280"
PROXY_URL = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
PROXY_PLUGIN_PATH = "proxy_auth_plugin.zip"

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD)



def connect_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def store_trending_topics(data):
    collection = connect_to_mongo()
    result = collection.insert_one(data)
    print("Data inserted with ID:", result.inserted_id)

def setup_driver(proxy_plugin_path=None):
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--enable-logging")
    # chrome_options.add_argument("--v=3")
    # chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--headless")

    if proxy_plugin_path:
        with zipfile.ZipFile(proxy_plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(proxy_plugin_path)

    service = Service("chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Login to X.com
def login_to_twitter(driver):
    driver.get("https://twitter.com/i/flow/login")
    # Step 1: Enter Email
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocapitalize=sentences]")))
    username_input = driver.find_element(By.CSS_SELECTOR, "input[autocapitalize=sentences]")
    username_input.send_keys(X_EMAIL)
    username_input.send_keys(Keys.RETURN)

    # Step 2: Enter Username
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid=ocfEnterTextTextInput]")))
        password_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid=ocfEnterTextTextInput]")
        password_input.send_keys(X_USERNAME)
        password_input.send_keys(Keys.RETURN)
    except:
        print("Username Not Needed")

    # Step 2: Enter Password
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,  "input[autocomplete=current-password]")))
    password_input = driver.find_element(By.CSS_SELECTOR, "input[autocomplete=current-password]")
    password_input.send_keys(X_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Step 3: Verify Login
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/head/title[contains(text(),'Home')]")))
        print("Login successful!")
    except:
        print("Login failed!")
    



# Fetch trending topics
def fetch_trending_topics(driver):
    WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div/div/div/div/div/div[2]/span")))

    trending_topics = []
    trend_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div/div/div/div/div/div[2]")
    for trend in trend_elements:
        if trend.text:
            trending_topics.append(trend.text)

    return trending_topics



# def save_page_source(driver, filename="page_source.html"):
#     with open(filename, "w", encoding="utf-8") as file:
#         file.write(driver.page_source)
#     print(f"Page source saved to {filename}")



def get_public_ip(proxy_url):
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    response = requests.get("http://ipinfo.io/ip", proxies=proxies)
    return response.text.strip()



if __name__ == "__main__":
    current_ip = get_public_ip(PROXY_URL)
    print("Current IP Address:", current_ip)
    driver = setup_driver()
    try:
        login_to_twitter(driver)
        time.sleep(10)
        # save_page_source(driver)
        trending = fetch_trending_topics(driver)
        # print("Trending Topics:", trending)

        record = {
            "_id": str(uuid.uuid4()),  # Generate a unique ID
            "trends": trending,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": current_ip,
        }
        # print("Storing data:", record)
        
        # Store in MongoDB
        store_trending_topics(record)
        # while True:
        #     time.sleep(1)
    finally:
        driver.quit()
