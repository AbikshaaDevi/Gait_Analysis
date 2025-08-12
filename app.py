from flask import Flask, render_template, request
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# 1️⃣ Load dataset
df = pd.read_csv("Gait_Data.csv")

# If 'leg' is numeric, create mapping for user-friendly input
leg_mapping = {1: "left", 2: "right"}
joint_mapping = {1: "hip", 2: "knee", 3: "ankle"}  # Change based on your dataset

# Reverse mapping for encoding during prediction
reverse_leg_mapping = {v: k for k, v in leg_mapping.items()}
reverse_joint_mapping = {v: k for k, v in joint_mapping.items()}

# 2️⃣ Features and target
X = df[['leg', 'joint', 'angle', 'velocity', 'acceleration']]
y = df['subject']

# 3️⃣ Train KNN Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form values
        leg_input = request.form["leg"].strip().lower()
        joint_input = request.form["joint"].strip().lower()
        angle = float(request.form["angle"])
        velocity = float(request.form["velocity"])
        acceleration = float(request.form["acceleration"])

        # Encode inputs using reverse mapping
        if leg_input not in reverse_leg_mapping:
            return render_template("index.html", prediction_text=f"Invalid leg value: '{leg_input}'. Allowed: {list(reverse_leg_mapping.keys())}")
        if joint_input not in reverse_joint_mapping:
            return render_template("index.html", prediction_text=f"Invalid joint value: '{joint_input}'. Allowed: {list(reverse_joint_mapping.keys())}")

        leg_val = reverse_leg_mapping[leg_input]
        joint_val = reverse_joint_mapping[joint_input]

        # Prepare features
        features = [[leg_val, joint_val, angle, velocity, acceleration]]

        # Predict
        prediction = model.predict(features)[0]

        return render_template("index.html", prediction_text=f"Predicted Person: {prediction}")

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
