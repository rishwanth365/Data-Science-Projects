from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#endpoint  = "http://localhost:8501/v1/models/potatoes_model:predict"
MODEL = tf.keras.models.load_model("saved_models/1.keras")
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "Hello, I am running"

def read_file_as_image(data):
    image = np.array(Image.open(BytesIO(data)))

    return image
@app.post("/predict/")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch=np.expand_dims(image,0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = round(100.0*np.max(predictions[0]),2)
    return {
        'class': predicted_class,
        'confidence': confidence  # Convert to percentage
    }


if __name__ == "__main__":
    uvicorn.run(app, host = 'localhost', port = 8000)