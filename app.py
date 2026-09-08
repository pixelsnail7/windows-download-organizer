from download_organizer import DownloadOrganizer
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/oragnize_files_api", methods=["POST"])
def trigger_organizer():
    try:
        DownloadOrganizer().organize_files()
        return jsonify({"success": True, "message": "Files organized successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/remove_empty_folders_api", methods=["POST"])
def trigger_remove_empty_folders():
    try:
        DownloadOrganizer().remove_empty_folders()
        return jsonify({"success": True, "message": "Removed empty folders successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/remove_duplicate_files", methods=["POST"])
def trigger_remove_duplicate_files():
    try:
        DownloadOrganizer().remove_duplicate_files()
        return jsonify({"success": True, "message": "Removed duplicate files successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)