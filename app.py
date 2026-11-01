from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from pathlib import Path
from datetime import datetime
import sqlite3

app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR / "shared_files"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "history.db"

SHARED_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Database
# --------------------------------------------------

def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            action TEXT NOT NULL,
            client_ip TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def log_activity(filename, action, client_ip):
    connection = get_db()

    connection.execute(
        """
        INSERT INTO history (filename, action, client_ip, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            filename,
            action,
            client_ip,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    connection.commit()
    connection.close()


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/")
def index():
    files = []

    for file_path in SHARED_DIR.iterdir():
        if file_path.is_file():
            files.append({
                "name": file_path.name,
                "size": file_path.stat().st_size,
            })

    connection = get_db()

    history = connection.execute(
        """
        SELECT *
        FROM history
        ORDER BY id DESC
        LIMIT 50
        """
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        files=files,
        history=history,
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return redirect(url_for("index"))

    filename = Path(uploaded_file.filename).name
    destination = SHARED_DIR / filename

    uploaded_file.save(destination)

    client_ip = request.remote_addr or "unknown"

    log_activity(
        filename,
        "UPLOAD",
        client_ip,
    )

    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download_file(filename):
    safe_filename = Path(filename).name

    client_ip = request.remote_addr or "unknown"

    log_activity(
        safe_filename,
        "DOWNLOAD",
        client_ip,
    )

    return send_from_directory(
        SHARED_DIR,
        safe_filename,
        as_attachment=True,
    )


# --------------------------------------------------
# Application entry point
# --------------------------------------------------

if __name__ == "__main__":
    initialize_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )