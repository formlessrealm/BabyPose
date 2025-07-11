from flask import Flask, render_template, request, send_file
import cv2
import mediapipe as mp
import joblib
import numpy as np
import os
from werkzeug.utils import secure_filename

# Setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load model
try:
    model = joblib.load("pose_model.pkl")
except Exception as e:
    print("❌ Модель ачаалахад алдаа гарлаа:", e)
    exit(1)


# MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
mp_drawing = mp.solutions.drawing_utils

# Route - Upload Page
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            result_path = analyze_pose(filepath)
            return send_file(result_path, mimetype='image/jpeg')

    return render_template("index.html")

# Pose анализ хийх функц
def analyze_pose(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        features = []
        for lm in landmarks:
            features.extend([lm.x, lm.y, lm.z, lm.visibility])

        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)[0]
        probas = model.predict_proba(features)[0]
        max_prob = np.max(probas)

        # Зураг дээр үр дүн бичих
        text = f'Pose: {prediction} ({max_prob * 100:.1f}%)'
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.rectangle(image, (10, 10), (500, 60), (0, 0, 0), -1)
        cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    else:
        cv2.putText(image, "⚠️ Pose not detected", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Save result
    result_path = os.path.join(UPLOAD_FOLDER, "result.jpg")
    cv2.imwrite(result_path, image)
    return result_path

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

