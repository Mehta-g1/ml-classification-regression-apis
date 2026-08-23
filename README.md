# Django Machine Learning API Project

A Django-based web application providing REST APIs to run predictions for 5 different datasets (Classification and Regression) using pre-trained Machine Learning models (4 models per dataset, total 20 combinations).

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
│   └── models.py             # Django database models
│
├── Datasets/                 # Source datasets used for training models
│   ├── Classification datasets/
│   │   ├── Diabetes/
│   │   └── Heart Disease/
│   └── Regression datasets/
│       ├── California Housing/
│       ├── Concrete Data/
│       └── Wine Quality/
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
│   │   └── Heart/            # Pickled models for heart disease prediction
|   |
│   └── Scalers/              # Standard scalers used for normalizing inputs
│       ├── diabetes_scaler.pkl
│       └── heart_scaler.pkl
│
├── Notebooks/                # Jupyter Notebooks used for model exploration & training
│   ├── Classification/
│   │   ├── diabetes.ipynb    # Model training and evaluation for diabetes
│   │   └── heart.ipynb       # Model training and evaluation for heart disease
│   └── Regression/           # Jupyter Notebooks for regression training
│
├── manage.py                 # Django command-line utility
└── requirements.txt          # Project dependencies (Django, pandas, scikit-learn, etc.)
```

---

## Machine Learning Models Supported

### Classification (Heart Disease, Diabetes)
1. **Logistic Regression** (Code: `1` or `LogisticRegression`)
2. **K-Neighbors Classifier (kNN)** (Code: `2` or `KNeighborsClassifier`)
3. **Decision Tree Classifier** (Code: `3` or `DecisionTreeClassifier`)
4. **Support Vector Classifier (SVC)** (Code: `4` or `SVC`)

### Regression (California Housing, Concrete, Wine Quality)
1. **Linear Regression** (Code: `1` or `LinearRegression`)
2. **K-Neighbors Regressor** (Code: `2` or `KNeighborsRegressor`)
3. **Decision Tree Regressor** (Code: `3` or `DecisionTreeRegressor`)
4. **Support Vector Regressor (SVR)** (Code: `4` or `SVR`)

---

## API Endpoints

All prediction API endpoints accept `POST` requests.

### 1. Predict Diabetes
* **URL:** `/predict/diabetes/`
* **Method:** `POST`
* **Required Parameters:**
  * `model-name`: String (`LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, or `SVC`)
  * `age`: Float/Int
  * `bmi`: Float
  * `family_history_diabetes`: `1` (Yes) or `0` (No)
  * `hypertension_history`: `1` (Yes) or `0` (No)
  * `glucose_fasting`: Float
  * `hba1c`: Float
  * `physical_activity_minutes_per_week`: Float/Int
  * `cardiovascular_history`: `1` (Yes) or `0` (No)
  * `gender`: String (`male`, `female`, or `other`)
  * `smoking_status`: String (`never`, `former`, etc.)

---

### 2. Predict Heart Disease
* **URL:** `/predict/heart/`
* **Method:** `POST`
* **Required Parameters:**
  * `model-name`: String (`LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, or `SVC`)
  * `age`: Int
  * `sex`: Int (`1` = Male, `0` = Female)
  * `cp`: Chest Pain type (`0` to `3`)
  * `trestbps`: Resting Blood Pressure
  * `chol`: Serum Cholestoral in mg/dl
  * `fbs`: Fasting Blood Sugar > 120 mg/dl (`1` = true, `0` = false)
  * `restecg`: Resting Electrocardiographic results (`0` to `2`)
  * `thalach`: Maximum heart rate achieved
  * `exang`: Exercise induced angina (`1` = yes, `0` = no)
  * `oldpeak`: ST depression induced by exercise
  * `slope`: The slope of the peak exercise ST segment (`0` to `2`)
  * `ca`: Number of major vessels colored by flourosopy (`0` to `4`)
  * `thal`: Thalassemia (`0` = normal, `1` = fixed defect, `2` = reversible defect)



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
