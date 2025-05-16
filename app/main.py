from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
from app.model import predict_digit_file
from app.database import init_db, save_prediction, save_feedback

app = FastAPI()

# Initialize DB
init_db()

#comment random

IMAGE_DIR = "../uploads"
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Digit Recognition API is running."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"error": "File must be an image."})

    try:
        # Save image to static folder
        image_id = str(uuid4())
        image_ext = file.filename.split('.')[-1]
        image_path = os.path.join(IMAGE_DIR, f"{image_id}.{image_ext}")

        with open(image_path, "wb") as f:
            f.write(await file.read())

        # Predict
        with open(image_path, "rb") as img_file:
            digit, confidence = predict_digit_file(img_file)

        # Store in DB
        prediction_id = save_prediction(digit, confidence, image_path)

        return {
            "prediction_id": prediction_id,
            "prediction": digit,
            "confidence": f"{confidence} %",
            "image_path": image_path
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/feedback")
async def give_feedback(
    prediction_id: str = Form(...),
    predicted: int = Form(...),
    real: int = Form(...),
    comment: str = Form(...)
):
    try:
        feedback_id = save_feedback(prediction_id, predicted, real, comment)
        return {"message": "Feedback saved", "feedback_id": feedback_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
