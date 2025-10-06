import os

BASE_URL = "https://www.pesuacademy.com/Academy"
LOGIN_PAGE_URL = f"{BASE_URL}/"
AUTH_URL = f"{BASE_URL}/j_spring_security_check"
CALENDAR_URL = f"{BASE_URL}/s/studentProfilePESUAdmin?menuId=668&controllerMode=6413&actionType=5"
TIMETABLE_URL = f"{BASE_URL}/s/studentProfilePESUAdmin?menuId=669&controllerMode=6415&actionType=5"
ATTENDANCE_URL = f"{BASE_URL}/s/studentProfilePESUAdmin"
ATTENDANCE_REFERER_URL = f"{BASE_URL}/s/studentProfilePESU"

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "a-strong-and-random-secret-key-for-sessions")

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ),
    "x-requested-with": "XMLHttpRequest",
}
