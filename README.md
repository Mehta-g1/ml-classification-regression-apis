# Django Machine Learning API Project

A Django-based web application providing REST APIs to run predictions for health metrics (specifically Heart Disease and Diabetes) using pre-trained Machine Learning classification models.

---

## Project Structure

Here is the complete project directory structure:

```text
ML Project/
│
├── APIs/                     # Django app containing API views and predictors
│   ├── predictor.py          # Core logic for loading pickled models/scalers and making predictions
│   ├── views.py              # API view handlers (validating inputs, parsing requests)
│   ├── urls.py               # API-specific URL routing
│   ├── apps.py               # Django app configuration
│   └── models.py             # Django database models (if any)
│
├── Datasets/                 # Datasets used for training models
│   ├── Classification datasets/
│   └── Regression datasets/
│
├── ML/                       # Django project main configuration directory
│   ├── settings.py           # Project settings (middleware, installed apps, database config)
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py / asgi.py     # Deployment entry points
│   └── __init__.py
│
├── ML_models and scalers/    # Pre-trained models and scaler pipelines (.pkl files)
│   ├── ML_Models/
│   │   ├── Diabetes/         # Pickled models for diabetes prediction
│   │   │   ├── Logistic_model.pkl
│   │   │   ├── kNN_model.pkl
│   │   │   ├── tree_model.pkl
│   │   │   └── svc_model.pkl
│   │   └── Heart/            # Pickled models for heart disease prediction
│   │       ├── Logistic_model.pkl
│   │       ├── kNN_model.pkl
│   │       ├── tree_model.pkl
│   │       └── svc_model.pkl
│   └── Scalers/              # Standard scalers used for normalizing inputs
│       ├── diabetes_scaler.pkl
│       └── heart_scaler.pkl
│
├── Notebooks/                # Jupyter Notebooks used for model exploration & training
│   ├── Classification/
│   │   ├── diabetes.ipynb    # EDA and classification model training for diabetes
│   │   └── heart.ipynb       # EDA and classification model training for heart disease
│   └── Regression/           # Placeholder for regression notebooks
│
├── manage.py                 # Django command-line utility
└── requirements.txt          # Project dependencies (Django, pandas, scikit-learn, etc.)
```

---

## Machine Learning Models Supported

The APIs support predictions using the following algorithms:
1. **Logistic Regression** (Code: `1` or `LogisticRegression`)
2. **K-Neighbors Classifier (kNN)** (Code: `2` or `KNeighborsClassifier`)
3. **Decision Tree Classifier** (Code: `3` or `DecisionTreeClassifier`)
4. **Support Vector Classifier (SVC)** (Code: `4` or `SVC`)

Each request can specify which model to run using the `model-name` parameter.

---

## API Endpoints

All prediction API endpoints accept `POST` requests.

### 1. Predict Diabetes
* **URL:** `/predict/diabetes/`
* **Method:** `POST`
* **Content-Type:** Form Data or URL Encoded
* **Required Parameters:**
  * `model-name`: String (`LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, or `SVC`)
  * `age`: Integer / Float
  * `bmi`: Float
  * `family_history_diabetes`: `1` (Yes) or `0` (No)
  * `hypertension_history`: `1` (Yes) or `0` (No)
  * `glucose_fasting`: Float
  * `hba1c`: Float
  * `physical_activity_minutes_per_week`: Integer
  * `cardiovascular_history`: `1` (Yes) or `0` (No)
  * `gender`: String (`male`, `female`, or `other`)
  * `smoking_status`: String (`never`, `former`, etc.)

* **Response Format (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "LogisticRegression",
    "output": {
      "Prediction": 0,
      "model-accuracy": {
        "sccuracy_score": 0.8847,
        "f1_score": 0.8946,
        "recall_score": 0.8175
      }
    }
  }
  ```

---

### 2. Predict Heart Disease
* **URL:** `/predict/heart/`
* **Method:** `POST`
* **Content-Type:** Form Data or URL Encoded
* **Required Parameters:**
  * `model-name`: String (`LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, or `SVC`)
  * `age`: Integer
  * `sex`: Integer (`1` = Male, `0` = Female)
  * `cp`: Chest Pain type (`0` to `3`)
  * `trestbps`: Resting Blood Pressure
  * `chol`: Serum Cholestoral in mg/dl
  * `fbs`: Fasting Blood Sugar > 120 mg/dl (`1` = true; `0` = false)
  * `restecg`: Resting Electrocardiographic results (`0` to `2`)
  * `thalach`: Maximum heart rate achieved
  * `exang`: Exercise induced angina (`1` = yes; `0` = no)
  * `oldpeak`: ST depression induced by exercise relative to rest
  * `slope`: The slope of the peak exercise ST segment (`0` to `2`)
  * `ca`: Number of major vessels colored by flourosopy (`0` to `4`)
  * `thal`: Thalassemia (`0` = normal; `1` = fixed defect; `2` = reversable defect)

* **Response Format (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "LogisticRegression",
    "output": {
      "Prediction": 1,
      "model-accuracy": {
        "accuracy_score": 0.7763,
        "recall_score": 0.8888,
        "f1_score": 0.7901
      }
    }
  }
  ```

---

## Installation & Running the Server

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (cmd):
.venv\Scripts\activate
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Run Migrations & Start Server
```bash
# Run database migrations
python manage.py migrate

# Run the Django development server
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.
