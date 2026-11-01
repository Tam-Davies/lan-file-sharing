from flask import Flask, render_template, request, send_from_directory, redirect, url_for, abort
from pathlib import Path
from datetime import datetime
import sqlite3

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR / "shared_files"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "history.db"

SHARED_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)

# Addresses belonging to the server machine.
SERVER_IPS = {
    "127.0.0.1",
    "::1",
    "172.20.10.2",
    "172.19.80.1",
}


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


def get_client_ip():
    return request.remote_addr or "unknown"


def is_server():
    return get_client_ip() in SERVER_IPS


def log_activity(filename, action, client_ip):
    connection = get_db()

    connection.execute(
        """
        INSERT INTO history
        (filename, action, client_ip, timestamp)
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


@app.route("/")
def index():

    files = []

    for file_path in SHARED_DIR.iterdir():
        if file_path.is_file():
            files.append({
                "name": file_path.name,
                "size": file_path.stat().st_size,
            })

    client_ip = get_client_ip()

    connection = get_db()

    if is_server():
        history = connection.execute(
            """
            SELECT *
            FROM history
            ORDER BY id DESC
            LIMIT 100
            """
        ).fetchall()

    else:
        # Clients only see their own download activity.
        history = connection.execute(
            """
            SELECT *
            FROM history
            WHERE client_ip = ?
            AND action = 'DOWNLOAD'
            ORDER BY id DESC
            LIMIT 50
            """,
            (client_ip,),
        ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        files=files,
        history=history,
        server=is_server(),
        client_ip=client_ip,
    )


@app.route("/upload", methods=["POST"])
def upload_file():

    # Only the server is allowed to upload.
    if not is_server():
        abort(403)

    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return redirect(url_for("index"))

    filename = Path(uploaded_file.filename).name

    destination = SHARED_DIR / filename

    uploaded_file.save(destination)

    log_activity(
        filename,
        "UPLOAD",
        get_client_ip(),
    )

    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download_file(filename):

    safe_filename = Path(filename).name

    file_path = SHARED_DIR / safe_filename

    if not file_path.exists() or not file_path.is_file():
        abort(404)

    client_ip = get_client_ip()

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


if __name__ == "__main__":

    initialize_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )