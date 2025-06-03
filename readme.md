# 🤖 Facebook Automation Bot

This Python-based bot automates commenting and replying to posts on Facebook using Selenium. It reads tasks from a `tasks.json` file and executes them using a headless or interactive Chrome browser session.

---

## 📁 Project Structure

```text
facebook-bot/
├── bot.py                 # Main script to read and process tasks
├── facebook_actions.py    # FacebookBot class with login, comment, and reply logic
├── config.py              # Contains credentials, paths, and logging config
├── tasks.json             # JSON file containing tasks to be performed
├── .env                   # (Optional) Environment variables for credentials
├── requirements.txt       # Python dependencies (to be created)
└── README.md              # Project documentation
```

---

## ⚙️ Features

- ✅ Login to Facebook via Selenium
- ✅ Post comments on specific posts
- ✅ Reply to specific comments by comment ID
- ✅ Reads tasks from `tasks.json`
- ✅ Logs all actions and errors
- ✅ Supports both normal and headless modes

---

## 📦 Requirements

- Python 3.7+
- Google Chrome (installed)
- ChromeDriver (auto-managed via `webdriver-manager`)

---

## 📥 Installation

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Add Credentials to .env**:

- Create a .env file
- Paste the following code

  ```bash
  FB_USERNAME=your_facebook_email
  FB_PASSWORD=your_facebook_password
  ```

  (Add your details in config.py file for now)

4. **Update the config.py file**:
   Update the `USER_DATA_DIR` and add the path to your chrome website

5. **🧪 Running the Bot**

   ```bash
   python bot.py
   ```

### This will:

- Log into Facebook using credentials from config.py or .env
- Read tasks from tasks.json
- Navigate to the relevant post
- Post a comment or reply based on the task details
- Log all actions to facebook_bot.log

---

## 📄 Logging

All actions and errors are logged to facebook_bot.log. You can configure log level and file location in config.py.

---

## 🔐 Security Note

Avoid hardcoding credentials in config.py. Use a .env file and dotenv for better security.

---
