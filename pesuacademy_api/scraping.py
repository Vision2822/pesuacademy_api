import re
import json
import requests
from bs4 import BeautifulSoup
from .config import (
    LOGIN_PAGE_URL, AUTH_URL, CALENDAR_URL, TIMETABLE_URL,
    ATTENDANCE_URL, ATTENDANCE_REFERER_URL, BASE_URL, BROWSER_HEADERS
)


def perform_login(username, password):
    session_obj = requests.Session()
    try:
        r_get = session_obj.get(LOGIN_PAGE_URL, headers=BROWSER_HEADERS)
        r_get.raise_for_status()
        soup = BeautifulSoup(r_get.text, 'html.parser')
        login_csrf = soup.find('input', {'name': '_csrf'})['value']

        payload = {'j_username': username, 'j_password': password, '_csrf': login_csrf}
        r_post = session_obj.post(AUTH_URL, data=payload, headers=BROWSER_HEADERS)
        r_post.raise_for_status()

        if "Bad credentials" in r_post.text:
            return None, "Invalid credentials"
        return session_obj, None
    except Exception as e:
        return None, str(e)


def get_semesters_and_csrf(session_obj, username):
    dashboard_res = session_obj.get(LOGIN_PAGE_URL, headers=BROWSER_HEADERS)
    soup = BeautifulSoup(dashboard_res.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    semester_options = soup.find_all('option')
    semesters = [{'id': opt['value'].strip('"'), 'name': opt.text} for opt in semester_options]
    student_name_tag = soup.find('span', class_='app-name-font')
    student_name = student_name_tag.text.strip().title() if student_name_tag else username
    return semesters, student_name, csrf_token


def get_attendance_data(session_obj, batch_id, csrf_token):
    res = session_obj.post(
        ATTENDANCE_URL,
        data={
            'controllerMode': '6415',
            'actionType': 8,
            'batchClassId': batch_id,
            'menuId': 660
        },
        headers={**BROWSER_HEADERS, "x-csrf-token": csrf_token, "Referer": ATTENDANCE_REFERER_URL},
    )
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    courses = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 4:
            try:
                attended, total = map(int, cols[2].text.strip().split('/'))
                courses.append({
                    'code': cols[0].text.strip(),
                    'name': cols[1].text.strip(),
                    'attended': attended,
                    'total': total,
                    'percentage': int(cols[3].text.strip())
                })
            except ValueError:
                continue
    return courses


def get_calendar_data(session_obj, csrf_token):
    headers = {**BROWSER_HEADERS, "x-csrf-token": csrf_token, "Referer": ATTENDANCE_REFERER_URL}
    res = session_obj.get(CALENDAR_URL, headers=headers)
    res.raise_for_status()
    match = re.search(r'var obj = JSON.parse\KATEX_INLINE_OPEN(.*?)\KATEX_INLINE_CLOSE;', res.text, re.DOTALL)
    if not match:
        raise ValueError("Could not parse calendar data.")
    return json.loads(match.group(1))


def get_structured_timetable(session_obj, csrf_token):
    headers = {**BROWSER_HEADERS, "x-csrf-token": csrf_token, "Referer": ATTENDANCE_REFERER_URL}
    res = session_obj.get(TIMETABLE_URL, headers=headers)
    res.raise_for_status()
    slots_match = re.search(r'var timeTableTemplateDetailsJson=(.*?);', res.text, re.DOTALL)
    schedule_match = re.search(r'var timeTableJson=(.*?);', res.text, re.DOTALL)
    if not (slots_match and schedule_match):
        raise ValueError("Could not parse timetable data.")
    slots_json = json.loads(slots_match.group(1))
    schedule_json = json.loads(schedule_match.group(1))

    slot_times = {s['orderedBy']: f"{s['startTime']} - {s['endTime']}" for s in slots_json}
    days_map = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}

    subjects_schedule = {}
    for key, value in schedule_json.items():
        if not key.startswith('ttDivText_'):
            continue
        parts = key.split('_')
        try:
            day_index = int(parts[1])
            slot_index = int(parts[2])
        except (IndexError, ValueError):
            continue

        if day_index not in days_map:
            continue
        class_time = slot_times.get(slot_index)
        if not class_time:
            continue

        subject_info = value[0].replace('ttSubject&&', '')
        subject_code = subject_info.split('-')[0]
        subject_name = '-'.join(subject_info.split('-')[1:])
        day_name = days_map[day_index]

        subjects_schedule.setdefault(subject_code, {'name': subject_name, 'schedule': {}})
        subjects_schedule[subject_code]['schedule'].setdefault(day_name, []).append(class_time)
    return subjects_schedule
