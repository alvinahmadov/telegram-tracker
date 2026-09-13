# Telegram Status Stealth Tracker

A lightweight Python application designed to check the online status of a specific Telegram contact via the MTProto API
without updating your own "online" status.

## Features

- **Stealth Mode**: Fetches contact status using Telethon without triggering your own activity update.
- **Anti-Spam Protection**: Built-in cooldown mechanism (`COOLDOWN_MINUTES`) to prevent frequent requests and handle
  Telegram `FloodWaitError` exceptions safely.
- **Structured Logging**: Automatic daily log rotation at midnight (`00:00`) with logs saved into a dedicated `logs/`
  directory using Loguru.
- **Time Calculation**: Automatically computes how long ago the contact was online in hours and minutes.

## File Structure

- `main.py`: Core script handling client initialization, anti-spam validation, and status checking.
- `logger.py`: Loguru setup providing console output and daily log file rotation.
- `utils.py`: Helper functions for time-ago calculations and user full-name formatting.
- `tluser_2.py`: Dataclass definitions for Telethon user objects and online status structures.

## Requirements

- Python 3.10+
- `Telethon==1.44.0`
- `python-dotenv==1.2.2`
- `loguru==0.7.3`

## Installation

1. **Clone the repository**:
    ```bash
    git clone [https://github.com/alvinahmadov/telegram-tracker.git](https://github.com/alvinahmadov/telegram-tracker.git)
    cd telegram-tracker
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a .env file in the root directory of the project.

```terminaloutput
API_ID=1234567
API_HASH=your_api_hash_from_my_telegram_org
APP_TITLE=TelegramTracker
COOLDOWN_MINUTES=5
TARGET_PHONE=+1234567890
TARGET_NAME=ContactName
```

* **API_ID** & **API_HASH**: Obtained from my.telegram.org
* **COOLDOWN_MINUTES**: Minimum interval between requests (enforced minimum is 2 minutes).
* **TARGET_PHONE**: International phone number of the target contact (including '+')

## Usage

Run the script manually:

```bash
python main.py
```

(Note: The first run will prompt you for your Telegram phone number and verification code/password to generate the
stealth_session.session file).

### Automation via Cron

To run the script automatically in the background every 10 minutes:

1. Open the crontab editor:
    ```bash
    crontab -e
   ``` 

2. Add the following line (replace /path/to/project with your absolute project path):
    ```bash
    */10 * * * * cd /path/to/project && /path/to/project/venv/bin/python main.py >/dev/null 2>&1
   ```