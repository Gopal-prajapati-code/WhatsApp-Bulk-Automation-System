# 📲 WhatsApp Bulk Automation System (v1.0)

A professional, web-based WhatsApp bulk messaging system built using **Python, Flask, and Selenium**, designed for controlled and safe bulk message delivery using WhatsApp Web.

---

## 🚀 Features

- 📊 Excel-based bulk messaging
- 👤 Personalized messages using `{name}` placeholders
- ⏱️ Configurable delays (human-like behavior)
- 🔁 Batch-wise message sending
- ⏸️ Pause & ▶ Resume functionality
- 📈 Live progress tracking dashboard
- ❌ Invalid number detection
- 🧾 Automatic success / failure logging
- ♻️ Retry-ready architecture
- 💾 Persistent WhatsApp session (QR scan only once)

---

## 🖥️ System Preview

### Dashboard
![Dashboard](screenshots/1.png)
<img width="1913" height="836" alt="image" src="https://github.com/user-attachments/assets/1d7e15c1-847d-4f9c-82e2-e089cc873436" />


### Bulk Messaging Panel
![Bulk Sender](screenshots/2.png)
<img width="1890" height="965" alt="image" src="https://github.com/user-attachments/assets/f8665ced-e33a-4299-ace5-603a6c06c382" />

### Send History
![History](screenshots/3.png)
<img width="1877" height="832" alt="image" src="https://github.com/user-attachments/assets/63a56dc2-356a-403f-87a0-ce76fe9279ce" />

> 📌 *Screenshots are for reference. Actual UI may vary based on browser and screen size.*

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Automation:** Selenium (WhatsApp Web)
- **Frontend:** HTML, Bootstrap 5
- **Data Handling:** Pandas, Excel
- **Browser:** Google Chrome

---

## 📂 Project Structure

WhatsApp-Bulk-Automation-System/
│── app.py
│── requirements.txt
│── state.json # runtime state (ignored in git)
│── send_report.csv # auto-generated logs
│
├── templates/
│ ├── base.html
│ ├── bulk.html
│ ├── dashboard.html
│ └── history.html
│
├── uploads/ # runtime uploads (ignored)
├── whatsapp_selenium_profile/ # WhatsApp session (ignored)
└── README.md

---

## 📑 Excel Format

The Excel file should contain the following columns:

3️⃣ Run the Application
python app.py

4️⃣ Open in Browser
http://127.0.0.1:5000

🧩 Chrome & ChromeDriver Installation Guide

This project requires Google Chrome and ChromeDriver to be installed and correctly configured.

1️⃣ Install Google Chrome

If Google Chrome is not already installed, download it from the official website:

🔗 Official Download Link
https://www.google.com/chrome/

After installation:

Open Chrome

Go to:

chrome://settings/help


Note the Chrome version number (example: 124.0.6367.xx)

2️⃣ Download ChromeDriver (VERY IMPORTANT)

ChromeDriver must match your installed Chrome version.

🔗 Official ChromeDriver Download Page
https://googlechromelabs.github.io/chrome-for-testing/

Steps:

Find your Chrome major version (example: 124)

Download chromedriver-win64.zip (for Windows)

Extract the ZIP file

You will get chromedriver.exe

3️⃣ Set ChromeDriver Path

Move chromedriver.exe to a permanent location, for example:

C:\Windows\chromedriver.exe


You may choose another folder, but ensure the path is updated in app.py.

4️⃣ Configure Paths in app.py

Open app.py and update the following configuration section:

# ================= CONFIG =================
CHROMEDRIVER_PATH = r"C:\Windows\chromedriver.exe"
USER_DATA_DIR = r"E:\Business client project\Whatsapp excel bulk project Web base\WhatsappWebApp\whatsapp_selenium_profile"

Configuration Explanation
Variable	Purpose
CHROMEDRIVER_PATH	Full path to the ChromeDriver executable
USER_DATA_DIR	Stores WhatsApp Web session (QR scan required only once)
5️⃣ Verify ChromeDriver Installation (Optional but Recommended)

Open Command Prompt and run:

chromedriver --version


Expected output example:

ChromeDriver 124.0.xxxx.xx


If command is not found, ensure:

Correct file path

ChromeDriver executable is accessible

6️⃣ First-Time WhatsApp Login

Start the application:

python app.py


Open browser:

http://127.0.0.1:5000


WhatsApp Web will open automatically

Scan QR code using your phone

Session will be saved in USER_DATA_DIR

📌 No QR scan required again unless USER_DATA_DIR is deleted

⚠️ Important Notes (Client Safety)

Do NOT delete USER_DATA_DIR after login

Do NOT share USER_DATA_DIR with anyone

This folder is intentionally excluded from GitHub using .gitignore

Chrome auto-update may require ChromeDriver update in future

🛡️ Common Issues & Fixes
Issue	Solution
Chrome opens then closes	ChromeDriver version mismatch
Session logged out	USER_DATA_DIR deleted
QR appears every time	Wrong USER_DATA_DIR path
Permission error	Run terminal as Administrator




