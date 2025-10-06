# 🧩 PESU Academy API

A clean, modular **Flask-based Python API** built to interact with PESU Academy data programmatically.

This project provides endpoints for login, attendance, timetable, and calendar retrieval.

---

## 🚀 Quick Start

```bash
git clone https://github.com/Vision2822/pesuacademy_api.git
cd pesuacademy_api
python -m venv venv
venv\Scripts\activate        # Windows
# or source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python -m pesuacademy_api.app
```
App runs on: **http://127.0.0.1:5000**

---

## 🧠 API Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/` | GET | Health check |
| `/api/login` | POST | Logs in with username & password |
| `/api/all_data` | GET | Returns attendance / timetable / calendar |
| `/api/logout` | GET | Ends session |

Example:
```bash
curl -X POST http://127.0.0.1:5000/api/login -d "username=SRN" -d "password=PASS"
```
## 🛠 Environment Variables
`FLASK_SECRET_KEY=<your-secret-key>`

---

## 📦 Optional: Local Install
```bash
pip install .
```
Then:
```python
from pesuacademy_api.app import app
app.run()
```

---

## ❤️ Credits
Built with Python 🐍 and Flask for educational purposes.

Vision2822
