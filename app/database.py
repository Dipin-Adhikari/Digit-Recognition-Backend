import sqlite3
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DB_PATH = os.getenv("DATABASE_URL")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # go one level up
DB_PATH = os.getenv("DATABASE_URL")

DB_PATH = os.path.join(BASE_DIR, DB_PATH)  # now this points to project_root/database/database.db

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Predictions table (unchanged)
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id TEXT PRIMARY KEY,
            prediction INTEGER,
            confidence INTEGER,
            image_path TEXT,
            created_at TEXT
        )
    ''')

    # Feedback table (no foreign key)
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id TEXT PRIMARY KEY,
            prediction_id TEXT,
            predicted INTEGER,
            real INTEGER,
            comment TEXT,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()

def save_prediction(prediction: int, confidence: int, image_path: str) -> str:
    pred_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions (id, prediction, confidence, image_path, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (pred_id, prediction, confidence, image_path, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return pred_id

def save_feedback(prediction_id: str, predicted: int, real: int, comment: str) -> str:
    feedback_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO feedback (id, prediction_id, predicted, real, comment, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (feedback_id, prediction_id, predicted, real, comment, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return feedback_id
