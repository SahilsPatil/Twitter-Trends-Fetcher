# 🐦 Twitter Trends Scraper

![image](https://github.com/user-attachments/assets/4f1e5a79-1483-41eb-8142-bd2d5c03fd10)

![image](https://github.com/user-attachments/assets/ef4f3b1c-1ba0-4d01-9712-991f505db63e)

![image](https://github.com/user-attachments/assets/d3dec210-9f07-415b-868c-17416677bbd4)





## 🚀 About the Project
This project automates fetching the top trending topics from **X.com (formerly Twitter)** using **Selenium** with a proxy setup for anonymity and stores the results in a **MongoDB** database. The project also includes an **Express.js server** to interact with the stored data and a **frontend** to display the results in real-time.

### 🎯 Key Features
- **Automated Trending Topics Fetching**: Uses Selenium to log in and fetch trending topics.
- **Proxy Support**: Ensures anonymity by routing requests through a proxy.
- **Data Storage**: Saves fetched data (trends, timestamp, IP) in MongoDB.
- **Frontend Interface**: View fetched data in real-time with interactive buttons.
- **Customizable**: Easily toggle headless mode or remove proxy configuration.

---

## 🗂️ Folder Structure

```plaintext
project-folder/
├── public/
│   └── index.html         # Frontend to display trends
├── python/
│   ├── chromedriver/      # Add your ChromeDriver here
│   ├── proxy_auth_plugin.zip  # Proxy plugin for authentication
│   └── main.py            # Python script for Selenium automation
├── server.js              # Backend API to run scripts and fetch data
└── README.md              # This file!
```

---

## 🛠️ Setup Instructions

### 1️⃣ Prerequisites
Make sure you have the following installed on your system:
- **Node.js**: [Download](https://nodejs.org/)
- **Python 3.x**: [Download](https://www.python.org/)
- **MongoDB**: [Download](https://www.mongodb.com/)
- **Google Chrome**: [Download](https://www.google.com/chrome/)
- **ChromeDriver**: [Download](https://chromedriver.chromium.org/)

### 2️⃣ Installation Steps

#### Clone the Repository
```bash
git clone https://github.com/SahilsPatil/Twitter-Trends-Fetcher.git
cd Twitter-Trends-Fetcher
```

#### Install Node.js Dependencies
```bash
npm install
```

#### Install Python Dependencies
```bash
pip install selenium pymongo requests
```

#### Configure MongoDB
Start your MongoDB server and ensure it's running on the default port (`27017`).

#### Add ChromeDriver
Place the compatible **ChromeDriver** in the `python/` folder.

#### Configure Proxy (Optional)
If you want to use a proxy:
1. Edit the `main.py` file and add your proxy credentials:
   ```python
   PROXY_USERNAME = "Your_PROXY_USERNAME"
   PROXY_PASSWORD = "Your_PROXY_PASSWORD"
   PROXY_HOST = "Your_PROXY_HOST"
   PROXY_PORT = "Your_PROXY_PORT"
   ```

2. If you **don't want to use a proxy**, remove the `proxy_plugin_path` from the `setup_driver()` function in `main.py`:
   ```python
   driver = setup_driver()  # Remove proxy_plugin_path
   ```

#### Configure X.com Credentials
Edit the `main.py` file and add your X.com (Twitter) credentials:
```python
X_USERNAME = "Your_X_Username"
X_EMAIL = "Your_X_EMAIL"
X_PASSWORD = "Your_X_PASS"
```

---


## ⚙️ How to Run the Project

### 1️⃣ Start the Backend Server
```bash
node server.js
```

### 2️⃣ Access the Frontend
Open the `index.html` file in your browser or access the server at:
```
http://localhost:3000
```

### 3️⃣ Fetch Trending Topics
- Click the **"Fetch Trending Topics"** button to run the Selenium script and fetch trending topics.
- View the results dynamically displayed on the page.

### 4️⃣ View JSON Data
- Click the **"Show Latest JSON"** button to view the stored data in JSON format.

---


## 🛠️ Customization Options

### ➡️ Enable/Disable Headless Mode
To enable or disable headless mode in **Selenium**, modify the `setup_driver()` function in `main.py`:
- **Enable**: Keep this line:
  ```python
  chrome_options.add_argument("--headless")
  ```
- **Disable**: Comment it out:
  ```python
  # chrome_options.add_argument("--headless")
  ```

---


## 📂 API Endpoints

### 1️⃣ Run Selenium Script
**POST** `/run-script`  
Runs the Selenium script to fetch trending topics and store them in MongoDB.

### 2️⃣ Fetch Latest Data
**GET** `/get-latest-data`  
Returns the latest stored data from MongoDB in JSON format.

---


## 🖥️ Frontend Preview

### 🎨 Features:
1. **Toggle Theme**: Switch between light and dark mode.
2. **Fetch Topics**: View trending topics dynamically.
3. **JSON Output**: Easily access stored data.

---


## 🤔 Troubleshooting

### Common Issues:
1. **ChromeDriver Compatibility**:
   - Ensure the ChromeDriver version matches your Chrome browser version.
2. **MongoDB Connection**:
   - Verify that MongoDB is running on `localhost:27017`.
3. **Proxy Authentication**:
   - Check proxy credentials in `main.py`.
