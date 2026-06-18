from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database Creation
def init_db():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Home Route
@app.route('/')
def home():
    return "Attendance Management System API"

# Add Attendance
@app.route('/attendance', methods=['POST'])
def add_attendance():
    data = request.json

    student_name = data['student_name']
    date = data['date']
    status = data['status']

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO attendance(student_name, date, status) VALUES (?, ?, ?)",
        (student_name, date, status)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Attendance Added Successfully"}), 201

# View All Attendance Records
@app.route('/attendance', methods=['GET'])
def get_attendance():

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM attendance")
    rows = cur.fetchall()

    conn.close()

    attendance_list = []

    for row in rows:
        attendance_list.append({
            "id": row[0],
            "student_name": row[1],
            "date": row[2],
            "status": row[3]
        })

    return jsonify(attendance_list)

# Update Attendance
@app.route('/attendance/<int:id>', methods=['PUT'])
def update_attendance(id):

    data = request.json
    status = data['status']

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE attendance SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Attendance Updated Successfully"})

# Delete Attendance
@app.route('/attendance/<int:id>', methods=['DELETE'])
def delete_attendance(id):

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM attendance WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Attendance Deleted Successfully"})

if __name__ == '__main__':
    app.run(debug=True)