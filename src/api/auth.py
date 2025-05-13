import pickle
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from requests import Session
from src.config.config import DATA_DIR

class FantraxAuth:
    COOKIE_PATH = DATA_DIR / "auth" / "fantraxloggedin.cookie"

    @classmethod
    def create_auth_session(cls) -> Session:
        """Creates and returns an authenticated session"""
        if not cls.COOKIE_PATH.exists():
            cls._generate_cookie_file()

        return cls._create_session_from_cookie()

    @classmethod
    def _generate_cookie_file(cls):
        """Generates a new cookie file through Selenium login"""
        print("Please login to Fantrax when the browser opens...")
        print("You have 30 seconds to complete the login.")

        # Ensure directory exists
        cls.COOKIE_PATH.parent.mkdir(parents=True, exist_ok=True)

        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--window-size=1920,1600")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")

        with webdriver.Chrome(service=service, options=options) as driver:
            driver.get("https://www.fantrax.com/login")
            time.sleep(30)  # Wait for manual login
            pickle.dump(driver.get_cookies(), open(cls.COOKIE_PATH, "wb"))

        print("Cookie file generated successfully!")

    @classmethod
    def _create_session_from_cookie(cls) -> Session:
        """Creates a session using saved cookie file"""
        session = Session()

        with open(cls.COOKIE_PATH, "rb") as f:
            for cookie in pickle.load(f):
                session.cookies.set(cookie["name"], cookie["value"])

        return session
