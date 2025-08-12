CREATE TABLE IF NOT EXISTS leave_records (
    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    leave_type TEXT CHECK(leave_type IN ('medical', 'optional', 'casual')),
    start_date TEXT,
    end_date TEXT,
    reason TEXT,
    status TEXT DEFAULT 'Pending',

    remaining_medical_leave INTEGER,
    remaining_optional_leave INTEGER,
    remaining_casual_leave INTEGER,

    FOREIGN KEY(user_id) REFERENCES users(id)
);
cur.execute("UPDATE leave_records SET status = 'Approved' WHERE id = ?", (leave_id,))
