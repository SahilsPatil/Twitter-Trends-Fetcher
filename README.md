# Twitter Trends Fetcher

![image](https://github.com/user-attachments/assets/4f1e5a79-1483-41eb-8142-bd2d5c03fd10)

![image](https://github.com/user-attachments/assets/ef4f3b1c-1ba0-4d01-9712-991f505db63e)

![image](https://github.com/user-attachments/assets/d3dec210-9f07-415b-868c-17416677bbd4)


# 🚀 Twitter Trends Scraper with Proxy & MongoDB

This project is a **Twitter Trends Scraper** that:
- 🕵️ Scrapes trending topics from **Twitter/X.com** using **Selenium**.
- 🌐 Supports **proxy integration** for anonymity.
- 🗃️ Stores the results in **MongoDB**.
- 🌟 Features a professional UI to view trends and JSON output dynamically.

---

## 🏗️ Folder Structure

```plaintext
├── public
│   └── index.html            # Frontend UI
├── python
│   ├── chromedriver          # Add your ChromeDriver here
│   ├── proxy_auth_plugin.zip # Proxy configuration (auto-generated)
│   └── main.py               # Selenium scraper script
├── server.js                 # Backend server to manage API
```

---

## ⚙️ Setup Instructions

### 1️⃣ **Prerequisites**
- **Python 3.8+** installed with the following libraries:
  - `pymongo`
  - `selenium`
  - `requests`
- **Node.js 14+** installed with the following libraries:
  - `express`
  - `mongoose`
- **MongoDB** installed (or use MongoDB Atlas for cloud-based storage).
- **ChromeDriver** that matches your version of the Chrome browser.

### 2️⃣ **Configuration**
- Add your **Twitter/X.com** and **Proxy credentials** in `python/main.py`:
  ```python
  # X.com (formerly Twitter) credentials
  X_USERNAME = "Your_X_Username"
  X_EMAIL = "Your_X_Email"
  X_PASSWORD = "Your_X_Password"

  # Proxy configuration
  PROXY_USERNAME = "Your_PROXY_Username"
  PROXY_PASSWORD = "Your_PROXY_Password"
  PROXY_HOST = "Your_PROXY_Host"
  PROXY_PORT = "Your_PROXY_Port"
  ```

### 🛠️ **Installation**




# Twitter-Trends-Fetcher
