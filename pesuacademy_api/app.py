from flask import Flask, request, session, jsonify
from .scraping import (
    perform_login, get_semesters_and_csrf,
    get_attendance_data, get_calendar_data, get_structured_timetable
)
from .config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/")
def index():
    return jsonify({"message": "PESU Academy API Running"})


@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form.get("username")
    password = request.form.get("password")
    _, error = perform_login(username, password)
    if error:
        return jsonify({"success": False, "error": error})
    session["username"] = username
    session["password"] = password
    return jsonify({"success": True})


@app.route("/api/all_data")
def api_all_data():
    if "username" not in session:
        return jsonify({"success": False, "error": "Not logged in"})
    try:
        username = session["username"]
        session_obj, error = perform_login(username, session["password"])
        if error:
            raise ValueError(error)
        semesters, student_name, csrf_token = get_semesters_and_csrf(session_obj, username)
        selected_batch_id = semesters[0]["id"] if semesters else None
        attendance = get_attendance_data(session_obj, selected_batch_id, csrf_token)
        calendar = get_calendar_data(session_obj, csrf_token)
        timetable = get_structured_timetable(session_obj, csrf_token)
        return jsonify({
            "success": True,
            "student_name": student_name,
            "attendance": attendance,
            "semesters": semesters,
            "calendar": calendar,
            "timetable": timetable,
        })
    except Exception as e:
        session.clear()
        return jsonify({"success": False, "error": str(e)})


@app.route('/api/logout')
def api_logout():
    session.clear()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
