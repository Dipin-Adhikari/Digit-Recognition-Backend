# Digit Recognition API 🔢

## 📌 Project Introduction

This is a **Digit Recognition backend API** built using **FastAPI**. It allows users to:

- Upload a handwritten digit image
- Receive the predicted digit with confidence score
- Submit feedback to improve model accuracy

The application stores the uploaded images on disk and uses **SQLite** to track predictions and feedback.

---

### 🔍 Demo Video

📽️ [Click here to watch the demo video](https://drive.google.com/file/d/1qnC3OMwMTExNB7tbLuzSO4nBkRs3Ec__/view?usp=sharing)

---

## 🧰 Tech Stack

- **FastAPI** – for building the RESTful API
- **TensorFlow** – for digit recognition model
- **OpenCV** – for preprocessing images
- **SQLite** – lightweight local database
- **Pytest** – for testing
- **Docker** – for containerization
- **GitHub Actions** – for CI/CD

---

## 📁 Folder Structure

```bash
root/
│
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── database.py        # SQLite DB connection and functions
│   └── model.py           # Load model and predict digit from image
│
├── database/
│   └── database.db        # SQLite database file
│
├── uploads/               # Uploaded images stored here
├── model/                 # Trained TensorFlow model
├── images/                # Sample image files
├── test/
│   └── test.py            # Pytest tests for API
│
├── .env                   # Environment variables (optional)
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies for app
├── requirements_test.txt  # Python dependencies for testing and CI/CD
```

---

## 🚀 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Dipin-Adhikari/Digit-Recognition-Backend.git
cd Digit-Recognition-Backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Run Tests

```bash
pytest test/test.py
```

---

## 🐳 Running with Docker

### 1. Build Docker Image

```bash
docker build -t digit-recognition-api .
```

### 2. Run Docker Container

```bash
docker run -d -p 8000:8000 digit-recognition-api
```

#### The API will be available at: http://localhost:8000

#### Docs will be available at: http://localhost:8000/docs

---

## 📫 API Endpoints

| Endpoint         | Method | Description                          |
| ---------------- | ------ | ------------------------------------ |
| `/predict`       | POST   | Predict digit from uploaded image    |
| `/feedback`      | POST   | Submit feedback on model prediction  |

## Endpoint Details

### `POST /predict`

Predicts a digit from an uploaded image.

| Parameter | Type       | Required | Description                |
| --------- | ---------- | -------- | -------------------------- |
| `file`    | UploadFile | Yes      | Image of handwritten digit |

**Example Response:**

```json
{
  "prediction_id": "uuid1234",
  "prediction": 7,
  "confidence": "96.32 %",
  "image_path": "../uploads/uuid1234.png"
}
```

### `POST /feedback`

Saves user feedback on a prediction.

| Parameter      | Type   | Required | Description                        |
| -------------- | ------ | -------- | ---------------------------------- |
| `prediction_id`| string | Yes      | ID of the prediction               |
| `predicted`    | int    | Yes      | Predicted digit                    |
| `real`         | int    | Yes      | Actual digit provided by user      |
| `comment`      | string | Yes      | User comments or corrections       |

**Example Response:**

```json
{
  "message": "Feedback saved",
  "feedback_id": "uuid5678"
}
```

---

## ✅ 12-Factor App Alignment

| Factor                 | Status | Explanation                                                     |
| ---------------------- | ------ | --------------------------------------------------------------- |
| I. Codebase            | ✅     | Single tracked repository                                       |
| II. Dependencies       | ✅     | Defined in `requirements.txt` and `requirements_test.txt`       |
| III. Config            | ✅     | `.env` used for sensitive values and config                     |
| IV. Backing Services   | ✅     | SQLite treated as an attached resource                          |
| V. Build, Release, Run | ✅     | Docker separates build/run steps                                |
| VI. Processes          | ✅     | Runs as a stateless FastAPI process                             |
| VII. Port Binding      | ✅     | Binds to port 8000                                              |
| VIII. Concurrency      | ⚠️     | Not explicitly scaled yet                                       |
| IX. Disposability      | ✅     | Fast startup/shutdown using Uvicorn                             |
| X. Dev/Prod Parity     | ⚠️     | SQLite is used in all stages; consider PostgreSQL in production |
| XI. Logs               | ⚠️     | Uses default Uvicorn logs; no centralized log management yet    |
| XII. Admin Processes   | ❌     | No separate admin tasks yet                                     |

---

## 📄 License

MIT License. Feel free to use and modify.
