from datetime import datetime
from flask import Flask, jsonify, render_template
from download_organizer import DownloadOrganizer
from pencil import Pencil


app = Flask(__name__)

# Helper function to append clean, timestamped logs
def log_event(message: str, level: str = "INFO") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if level == "SUCCESS":
        Pencil.add("./static/info.log", f"[<span class='time'>{timestamp}</span>] [<span class='success'>{level}</span>] {message}<br>")
    elif level == "error":
        Pencil.add("info.log", f"[<span class='time'>{timestamp}</span>] [<span class='error'>{level}</span>] {message}<br>")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/oragnize_files_api", methods=["POST"])
def trigger_organizer():
    try:
        DownloadOrganizer().organize_files()
        msg = "Files organized successfully!"
        log_event(msg, level="SUCCESS")
        return jsonify({"success": True, "message": msg}), 200
    except Exception as e:
        error_msg = str(e)
        log_event(f"Failed to organize files: {error_msg}", level="ERROR")
        return jsonify({"success": False, "error": error_msg}), 500


@app.route("/remove_empty_folders_api", methods=["POST"])
def trigger_remove_empty_folders():
    try:
        DownloadOrganizer().remove_empty_folders()
        msg = "Removed empty folders successfully!"
        log_event(msg, level="SUCCESS")
        return jsonify({"success": True, "message": msg}), 200
    except Exception as e:
        error_msg = str(e)
        log_event(f"Failed to remove empty folders: {error_msg}", level="ERROR")
        return jsonify({"success": False, "error": error_msg}), 500


@app.route("/remove_duplicate_files_api", methods=["POST"])
def trigger_remove_duplicate_files():
    try:
        DownloadOrganizer().remove_duplicate_files()
        msg = "Removed duplicate files successfully!"
        log_event(msg, level="SUCCESS")
        return jsonify({"success": True, "message": msg}), 200
    except Exception as e:
        error_msg = str(e)
        log_event(f"Failed to remove duplicate files: {error_msg}", level="ERROR")
        return jsonify({"success": False, "error": error_msg}), 500


if __name__ == "__main__":
    app.run(debug=True)