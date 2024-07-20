from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import os
import traceback

app = Flask(__name__)

# Load model and preprocessor
PREPROCESSING_PATH = r'artifact\testing\preprocessor.pkl'
MODEL_PATH = r'artifact\testing\model.pkl'

preprocessor = joblib.load(PREPROCESSING_PATH)
model = joblib.load(MODEL_PATH)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Extract form data
        data = {
            "continent": [request.form["continent"]],
            "education_of_employee": [request.form["education_of_employee"]],
            "has_job_experience": [request.form["has_job_experience"]],
            "requires_job_training": [request.form["requires_job_training"]],
            "no_of_employees": [request.form["no_of_employees"]],
            "company_age": [request.form["company_age"]],
            "region_of_employment": [request.form["region_of_employment"]],
            "prevailing_wage": [request.form["prevailing_wage"]],
            "unit_of_wage": [request.form["unit_of_wage"]],
            "full_time_position": [request.form["full_time_position"]]
        }
        
        input_df = pd.DataFrame(data)

        # Preprocess the data
        preprocessed_data = preprocessor.transform(input_df)

        # Make prediction
        prediction = model.predict(preprocessed_data)[0]

        # Determine result
        result = "Visa-approved" if prediction == 1 else "Visa Not-Approved"

        return render_template("index.html", result=result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
