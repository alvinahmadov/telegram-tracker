import asyncio
import os
import time

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError

from logger import custom_logger
from tluser import User
from utils import get_time_ago, get_fullname

load_dotenv()

# Rate-limiting settings
COOLDOWN_MINUTES_MIN = 2
COOLDOWN_FILE = ".cooldown_lock"

# Receive and check data
try:
    API_ID: int = int(os.getenv('API_ID'))
    API_HASH: str = os.getenv('API_HASH')
    APP_TITLE: str = os.getenv('APP_TITLE')
    
    COOLDOWN_MINUTES: int = int(os.getenv('COOLDOWN_MINUTES', default=5))
    
    TARGET_PHONE: str | None = os.getenv('TARGET_PHONE')
    TARGET_NAME: str = os.getenv('TARGET_NAME', default=TARGET_PHONE)
    
    if COOLDOWN_MINUTES < COOLDOWN_MINUTES_MIN:
        COOLDOWN_MINUTES = COOLDOWN_MINUTES_MIN
except TypeError:
    custom_logger.error("❌ Error: Check that the .env file exists and contains API_ID, API_HASH and TARGET_PHONE.")
    exit(1)


def check_cooldown() -> int:
    """Checks whether enough time has passed since the last run."""
    if os.path.exists(COOLDOWN_FILE):
        with open(COOLDOWN_FILE, "r") as f:
            try:
                last_run = float(f.read().strip())
                elapsed = time.time() - last_run
                cooldown_seconds = COOLDOWN_MINUTES * 60
                
                if elapsed < cooldown_seconds:
                    remaining_sec = int(cooldown_seconds - elapsed)
                    return remaining_sec
            except ValueError:
                pass
    
    # If the cooldown has passed, update the file with the new time
    with open(COOLDOWN_FILE, "w") as f:
        f.write(str(time.time()))
    return 0


async def main():
    # Checking the timer before executing any logic
    remaining_wait = check_cooldown()
    if remaining_wait > 0:
        minutes_left = remaining_wait // 60
        seconds_left = remaining_wait % 60
        print(
            f"⏳ Too frequent requests.\n"
            f"Anti-spam protection is active.\n"
            f"Wait {minutes_left} min. {seconds_left} sec."
        )
        return
    
    custom_logger.info(f"=== Running {APP_TITLE} ===")
    async with TelegramClient('stealth_session', API_ID, API_HASH) as client:
        custom_logger.info(f"Requesting a status for a contact: {TARGET_NAME}...")
        
        try:
            # Telethon will automatically find the user by number if he is in your contacts
            user: User = await client.get_entity(TARGET_PHONE)
            status = user.status
            fullname = get_fullname(user, TARGET_NAME)
            status_type = type(status).__name__
            
            if status_type == 'UserStatusOffline':
                local_time = status.was_online.astimezone().strftime('%d.%m.%Y %H:%M')
                time_ago = get_time_ago(user.status)
                custom_logger.success(f"✅ {fullname} was online: {local_time} ({time_ago})")
            elif status_type == 'UserStatusOnline':
                custom_logger.success(f"🟢 {fullname} now online")
            else:
                custom_logger.warning(f"⚠️ Status is hidden (current value: {status_type}).")
        
        except FloodWaitError as e:
            custom_logger.error(f"⛔ Telegram has temporarily blocked requests! Wait required: {e.seconds} seconds.")
        except ValueError:
            custom_logger.error(
                f"❌ Error: Contact number {TARGET_PHONE} not found."
                f"Make sure contact is in your Telegram address book."
            )
        except Exception as e:
            custom_logger.error(f"❌ An unexpected error occurred: {e}")
        
        finally:
            if remaining_wait == 0:
                custom_logger.info("-" * 45)


if __name__ == '__main__':
    # On Windows sometimes an EventLoop error occurs, this solves the problem:
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
