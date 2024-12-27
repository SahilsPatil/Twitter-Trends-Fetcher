from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests

X_USERNAME = "rohan249617897"
X_EMAIL = "abidan.daltyn@finestudio.org"
X_PASSWORD = "Rohan@1234"
PROXY_USERNAME = "abidan"
PROXY_HOST = "in.proxymesh.com"
PROXY_PORT = "31280"

# Path to the proxy authentication plugin zip file
PROXY_PLUGIN_PATH = "proxy_auth_plugin.zip"
PROXY_URL = f"http://{PROXY_USERNAME}:{PROXY_USERNAME}@{PROXY_HOST}:{PROXY_PORT}"


def setup_driver(proxy_plugin_path):
    """Sets up the Selenium WebDriver with the proxy authentication plugin."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--ignore-certificate-errors")

    # Add the proxy authentication plugin
    # chrome_options.add_argument(f'--proxy-server={PROXY_URL}')
    chrome_options.add_extension(proxy_plugin_path)

    # Specify the path to your ChromeDriver
    service = Service("chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def handle_proxy_auth_popup(driver):
    try:
        # Wait for the authentication dialog to appear (increase timeout)
        WebDriverWait(driver, 920).until(EC.alert_is_present())  # Increased timeout to 20 seconds
        alert = Alert(driver)
        alert.send_keys(f"{PROXY_USERNAME}{Keys.TAB}{PROXY_USERNAME}")  # Add username and password
        alert.accept()  # Accept the popup after entering credentials
        print("Proxy authentication successful.")
    except Exception as e:
        print(f"Error handling proxy authentication: {e}")


def login_to_twitter(driver):
    """Logs into Twitter/X with the provided credentials."""
    driver.get("https://x.com/i/flow/login")
    # handle_proxy_auth_popup(driver)

    try:
        # Step 1: Enter Email
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocapitalize=sentences]"))
        )
        email_input = driver.find_element(By.CSS_SELECTOR, "input[autocapitalize=sentences]")
        email_input.send_keys(X_EMAIL)
        email_input.send_keys(Keys.RETURN)

        # Step 2: Enter Username
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid=ocfEnterTextTextInput]"))
        )
        username_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid=ocfEnterTextTextInput]")
        username_input.send_keys(X_USERNAME)
        username_input.send_keys(Keys.RETURN)

        # Step 3: Enter Password
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete=current-password]"))
        )
        password_input = driver.find_element(By.CSS_SELECTOR, "input[autocomplete=current-password]")
        password_input.send_keys(X_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        # Step 4: Verify Login
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//title[contains(text(),'Home')]"))
        )
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")


def fetch_trending_topics(driver):
    """Fetches trending topics from Twitter/X."""
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now']"))
        )

        trending_xpath = "//div[@aria-label='Timeline: Trending now']//span"
        trend_elements = driver.find_elements(By.XPATH, trending_xpath)

        trending_topics = [trend.text for trend in trend_elements if trend.text]
        return trending_topics
    except Exception as e:
        print(f"Failed to fetch trending topics: {e}")
        return []


def get_public_ip(proxy_url):
    """Fetches the public IP address using the specified proxy."""
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    try:
        response = requests.get("http://ipinfo.io/ip", proxies=proxies)
        return response.text.strip()
    except Exception as e:
        print(f"Failed to fetch IP address: {e}")
        return None


if __name__ == "__main__":
    # Set the proxy URL (from the proxy_auth_plugin)
    

    # Fetch and print the current public IP address
    current_ip = get_public_ip(PROXY_URL)
    if current_ip:
        print("Current IP Address:", current_ip)

    # Setup WebDriver with the proxy authentication plugin
    driver = setup_driver(PROXY_PLUGIN_PATH)

    try:
        # Login to Twitter/X
        login_to_twitter(driver)

        # Pause to allow page loading
        time.sleep(15)

        # Fetch and display trending topics
        # trending_topics = fetch_trending_topics(driver)
        # print("Trending Topics:", trending_topics)
    finally:
        driver.quit()


