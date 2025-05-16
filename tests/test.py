import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Array of image paths and their expected labels
test_images = [
    {"path": "images/1.jpg", "label": 1},
    {"path": "images/2.jpg", "label": 2},
    {"path": "images/4.jpg", "label": 4},
    {"path": "images/5.jpg", "label": 5},
    {"path": "images/6.jpg", "label": 6},
    {"path": "images/7.jpg", "label": 7},
    {"path": "images/8.jpg", "label": 8},
    {"path": "images/9.jpg", "label": 9}
]

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Digit Recognition API is running."}

@pytest.mark.parametrize("test_case", test_images)
def test_predict_and_feedback(test_case):
    image_path = test_case["path"]
    expected_label = test_case["label"]

    # Ensure the image exists
    assert os.path.exists(image_path), f"Image not found: {image_path}"

    # POST to /predict
    with open(image_path, "rb") as img:
        response = client.post("/predict", files={"file": (os.path.basename(image_path), img, "image/jpeg")})

    assert response.status_code == 200
    data = response.json()

    assert "prediction_id" in data
    assert "prediction" in data
    assert "confidence" in data

    prediction_id = data["prediction_id"]
    predicted = data["prediction"]

    # POST to /feedback
    feedback_data = {
        "prediction_id": prediction_id,
        "predicted": predicted,
        "real": expected_label,
        "comment": f"Test feedback for image {os.path.basename(image_path)}"
    }

    feedback_response = client.post("/feedback", data=feedback_data)
    assert feedback_response.status_code == 200
    feedback_json = feedback_response.json()
    assert "feedback_id" in feedback_json
