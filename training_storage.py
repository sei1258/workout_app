import json
import os
from pathlib import Path


DATA_DIR = Path(
    os.environ.get(
        "FLET_APP_STORAGE_DATA",
        Path.home() / ".workout_app",
    )
)

DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE = DATA_DIR / "workout_app_data.json"


def load_training():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_training(training_records):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            training_records,
            file,
            ensure_ascii=False,
            indent=2,
        )