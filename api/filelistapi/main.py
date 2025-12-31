import os
import logging
from flask import Flask, jsonify, Response, request
from typing import Literal, TypeAlias

LOG_FILE: str = "logs/api_access.log"

# Create the logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

FlaskReturn: TypeAlias = (
    tuple[Response, Literal[400]] |
    tuple[Response, Literal[404]] |
    tuple[Response, Literal[403]] |
    tuple[Response, Literal[500]] |
    Response
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # logs to console
    ]
)

app = Flask(__name__)

def get_directory_contents(base: str, path: str) -> FlaskReturn:
    """Get the contents of a directory with logging and secure path checks."""
    logging.info(f"Request from {request.remote_addr} to access path: {path}")

    full_path: str = os.path.abspath(os.path.join(base, path))

    if not full_path.startswith(os.path.abspath(base)):
        logging.warning(f"ACCESS DENIED: Attempt to escape base path: {full_path}")
        return jsonify({"error": "access denied"}), 403

    if not os.path.exists(full_path):
        logging.warning(f"NOT FOUND: Path does not exist: {full_path}")
        return jsonify({"error": "not found"}), 404

    if os.path.isdir(full_path):
        contents = []
        try:
            for entry in os.listdir(full_path):
                item_path = os.path.join(full_path, entry)
                contents.append({
                    "name": entry,
                    "is_file": os.path.isfile(item_path),
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else -1
                })
        except Exception as e:
            logging.error(f"ERROR: Failed to list contents of {full_path}: {e}")
            return jsonify({"error": "internal server error"}), 500

        logging.info(f"SUCCESS: Listed directory {full_path}")
        return jsonify({"contents": contents})
    else:
        size = os.path.getsize(full_path)
        logging.info(f"SUCCESS: Retrieved file info: {full_path} ({size} bytes)")
        return jsonify({"file": path, "size": size})


@app.route("/downloads/", defaults={"path": ""})
@app.route("/downloads/<path:path>")
def list_dir(path: str) -> FlaskReturn:
    base: str = "/mnt/hdd_001/website/downloads"
    return get_directory_contents(base, path)

# @app.route("/api/public/", defaults={"path": ""})
# @app.route("/api/public/<path:path>")
# def list_dir_public(path: str) -> FlaskReturn:
#     base: str = "/mnt/hdd_001/website/downloads/public"
#     return get_directory_contents(base, path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
