import time
import uuid
import requests
import zipfile
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# MongoDB Setup
MONGO_URI = "mongodb://localhost:27017/"  # Update for your MongoDB setup
DB_NAME = "twitter_trends"
COLLECTION_NAME = "trends"

# X.com (formerly Twitter) credentials
X_USERNAME = "Your_X_Username"
X_EMAIL = "Your_X_EMAIL"
X_PASSWORD = "Your_X_PASS"

# Proxy configuration
PROXY_USERNAME = "Your_PROXY_USERNAME"
PROXY_PASSWORD = "Your_PROXY_PASSWORD"
PROXY_HOST = "Your_PROXY_HOST"
PROXY_PORT = "Your_PROXY_PORT"
PROXY_URL = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
PROXY_PLUGIN_PATH = "proxy_auth_plugin.zip"


# Chrome Proxy Plugin
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


# MongoDB connection
def connect_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


# Store trending topics in MongoDB
def store_trending_topics(data):
    collection = connect_to_mongo()
    result = collection.insert_one(data)
    print("Data inserted with ID:", result.inserted_id)


# Set up Chrome WebDriver
def setup_driver(proxy_plugin_path=None):
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--headless")

    if proxy_plugin_path:
        with zipfile.ZipFile(proxy_plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(proxy_plugin_path)

    service = Service("python/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Login to X.com (formerly Twitter)
def login_to_twitter(driver):
    driver.get("https://twitter.com/i/flow/login")
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocapitalize=sentences]")))
    
    # Enter Email
    username_input = driver.find_element(By.CSS_SELECTOR, "input[autocapitalize=sentences]")
    username_input.send_keys(X_EMAIL)
    username_input.send_keys(Keys.RETURN)

    # Enter Username (if needed)
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid=ocfEnterTextTextInput]")))
        password_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid=ocfEnterTextTextInput]")
        password_input.send_keys(X_USERNAME)
        password_input.send_keys(Keys.RETURN)
    except:
        print("Username step skipped.")

    # Enter Password
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete=current-password]")))
    password_input = driver.find_element(By.CSS_SELECTOR, "input[autocomplete=current-password]")
    password_input.send_keys(X_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Verify Login
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


# Get public IP address via proxy
def get_public_ip(proxy_url):
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    response = requests.get("http://ipinfo.io/ip", proxies=proxies)
    return response.text.strip()


# Main execution
if __name__ == "__main__":
    # Get public IP
    current_ip = get_public_ip(PROXY_URL)
    print("Current IP Address:", current_ip)
    
    # Set up the WebDriver
    driver = setup_driver(proxy_plugin_path=PROXY_PLUGIN_PATH) #proxy_plugin_path=PROXY_PLUGIN_PATH
    
    try:
        # Log in to X.com (formerly Twitter)
        login_to_twitter(driver)
        time.sleep(10)
        
        # Fetch trending topics
        trending = fetch_trending_topics(driver)

        # Prepare the record to be stored in MongoDB
        record = {
            "_id": str(uuid.uuid4()),  # Generate a unique ID
            "trends": trending,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": current_ip,
        }

        # Store the trending topics in MongoDB
        store_trending_topics(record)

    finally:
        # Close the WebDriver
        driver.quit()
