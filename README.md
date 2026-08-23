# Django Machine Learning API Project

A production-ready Django web application providing REST APIs to run predictions for three different datasets (Classification and Regression) using pre-trained Machine Learning models. The application supports a unified input interface, accepting both **JSON payloads** (`application/json`) and **Form-Data** / **URL-Encoded** payloads, backed by fast-fail input validation.

---

## Project Structure & Files

Here is the complete project directory structure with explanations of the primary components:

```text
ML Project/
│
├── APIs/                       # Django application package for API views & logic
│   ├── predictor.py            # Contains ML prediction wrappers that load pickeled scalers and models
│   ├── views.py                # Endpoint request handlers; parses formats, validates fields, catches errors
│   ├── urls.py                 # App-level routing mapping endpoints to views
│   ├── apps.py                 # App configuration registry
│   └── models.py               # Django DB models (unused, stateless architecture)
│
├── Datasets/                   # Raw training data sourced from Notebook training
│   ├── Classification datasets/
│   │   ├── Diabetes/           # diabetes_dataset.csv
│   │   └── Heart Disease/      # heart.csv
│   └── Regression datasets/
│       └── California Housing/ # california_housing.csv
│
├── ML/                         # Project settings package
│   ├── settings.py             # Global Django configurations, middleware, and installed apps
│   ├── urls.py                 # Root URL router (routes /predict/* to APIs.urls)
│   ├── wsgi.py / asgi.py       # WSGI/ASGI gateways for deployment servers
│   └── __init__.py
│
├── ML_models and scalers/      # Binary serialized model pipelines (.pkl format)
│   ├── ML_Models/
│   │   ├── Diabetes/           # Pickled classifiers (Logistic Regression, kNN, Decision Tree, SVC)
│   │   ├── Heart/              # Pickled classifiers (Logistic Regression, kNN, Decision Tree, SVC)
│   │   └── California_Housing/ # Pickled regressors (Linear Regression, Ridge, kNN, Tree, SVR)
│   └── Scalers/                # Scikit-learn StandardScaler/preprocessing pipelines
│       ├── diabetes_scaler.pkl
│       ├── heart_scaler.pkl
│       └── california_housing.pkl
│
├── Notebooks/                  # Research, modeling, and training notebooks
│   ├── Classification/
│   │   ├── diabetes.ipynb      # Training & evaluation of classification models for Diabetes
│   │   └── heart.ipynb         # Training & evaluation of classification models for Heart Disease
│   └── Regression/
│       └── california_housing.ipynb # Training & evaluation of regression models for housing price index
│
├── manage.py                   # Django CLI administrative entry point
└── requirements.txt            # System dependencies (Django, pandas, scikit-learn, etc.)
```

---

## Machine Learning Models Supported

### Classification (Heart Disease, Diabetes)
1. **Logistic Regression** (Name: `LogisticRegression`)
2. **K-Neighbors Classifier (kNN)** (Name: `KNeighborsClassifier`)
3. **Decision Tree Classifier** (Name: `DecisionTreeClassifier`)
4. **Support Vector Classifier (SVC)** (Name: `SVC`)

### Regression (California Housing)
1. **Linear Regression** (Name: `LinearRegression`)
2. **Ridge Regression** (Name: `Ridge`)
3. **K-Neighbors Regressor** (Name: `KNeighborsRegressor`)
4. **Decision Tree Regressor** (Name: `DecisionTreeRegressor`)
5. **Support Vector Regressor (SVR)** (Name: `SVR`)

---

## Request Formats & Payload Flexibility

All endpoints support two request payload types:
1. **JSON Payload** (`Content-Type: application/json`):
   ```json
   {
     "model-name": "LogisticRegression",
     "age": 58,
     ...
   }
   ```
2. **Form-Data / URL-Encoded** (`Content-Type: application/x-www-form-urlencoded` or `multipart/form-data`):
   Key-value pairs sent in the POST request body.

> [!NOTE]
> All endpoints are restricted to the `POST` method. Any `GET` requests will automatically return `405 Method Not Allowed`.

---

## API Endpoints & Dataset Examples

### 1. Predict Diabetes
* **URL:** `/predict/diabetes/`
* **Method:** `POST`
* **Validation Rules:**
  * Categorical mapping is automatically applied for `gender` (converted to dummy columns `gender_Male`, `gender_Other`) and `smoking_status` (converted to `smoking_status_Former`, `smoking_status_Never`).
  * Features `family_history_diabetes` and `hypertension_history` require string values `'1'` (Yes) or `'0'` (No).
* **Dataset Example (From `diabetes.ipynb` Index 0):**
  ```json
  {
    "model-name": "LogisticRegression",
    "age": "58",
    "bmi": "30.0",
    "family_history_diabetes": "0",
    "hypertension_history": "0",
    "glucose_fasting": "136",
    "hba1c": "8.18",
    "physical_activity_minutes_per_week": "215",
    "cardiovascular_history": "0",
    "gender": "Male",
    "smoking_status": "Never"
  }
  ```
* **Sample 200 Response:**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "LogisticRegression",
    "output": {
      "Prediction": 1,
      "model-accuracy": {
        "sccuracy_score": 0.8847,
        "f1_score": 0.8946069469835466,
        "recall_score": 0.8175591011611394
      }
    }
  }
  ```

---

### 2. Predict Heart Disease
* **URL:** `/predict/heart/`
* **Method:** `POST`
* **Dataset Example (From `heart.ipynb` Index 941):**
  ```json
  {
    "model-name": "LogisticRegression",
    "age": "52",
    "sex": "0",
    "cp": "2",
    "trestbps": "136",
    "chol": "196",
    "fbs": "0",
    "restecg": "0",
    "thalach": "169",
    "exang": "0",
    "oldpeak": "0.1",
    "slope": "1",
    "ca": "0",
    "thal": "2"
  }
  ```
* **Sample 200 Response:**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "LogisticRegression",
    "output": {
      "Prediction": 1,
      "model-accuracy": {
        "accuracy_score": 0.7763157894736842,
        "recall_score": 0.8888888888888888,
        "f1_score": 0.7901234567901234
      }
    }
  }
  ```

---

### 3. Predict California Housing Prices
* **URL:** `/predict/california-housing/`
* **Method:** `POST`
* **Dataset Example (From `california_housing.ipynb` Index 0):**
  ```json
  {
    "model-name": "LinearRegression",
    "MedInc": "8.3252",
    "HouseAge": "41.0",
    "AveRooms": "6.984127",
    "AveBedrms": "1.023810",
    "Population": "322.0",
    "AveOccup": "2.555556",
    "Latitude": "37.88",
    "Longitude": "-122.23"
  }
  ```
* **Sample 200 Response:**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "LinearRegression",
    "output": {
      "Prediction": 4.126220702280297,
      "model-accuracy": {
        "r2_score": 0.6009790143129108,
        "mean_absolute_error": 0.5366527228153435,
        "mean_squared_error": 0.5444842122132871
      }
    }
  }
  ```

---

## Standard Error Response Structures

### 1. HTTP 400 Bad Request
Occurs if the `model-name` parameter is missing or has an unsupported value.
* **Response Content:**
  ```json
  {
    "status": "Bad Request",
    "message": "Wrong Model Name: 'InvalidModel'. Available options: ['LogisticRegression', 'KNeighborsClassifier', 'DecisionTreeClassifier', 'SVC']",
    "model-name": "InvalidModel",
    "output": {
      "model_id": null,
      "prediction": "null"
    }
  }
  ```

### 2. HTTP 422 Unprocessable Entity
Occurs if required fields are missing or cannot be parsed into numeric values.
* **Response Content:**
  ```json
  {
    "status": "Unprocessable Entity",
    "message": "Input validation failed. Please check the errors field for details.",
    "errors": [
      "Field 'age' is required.",
      "Field 'bmi' must be numeric (received: 'invalid_text')."
    ],
    "model-name": "LogisticRegression",
    "output": {
      "model_id": 1,
      "prediction": "null"
    }
  }
  ```

### 3. HTTP 405 Method Not Allowed
Occurs if a method other than `POST` (e.g. `GET`) is sent to the endpoint.
* **Response Content:**
  ```html
  <h1>Method Not Allowed (GET)</h1>
  ```

### 4. HTTP 500 Internal Server Error
Occurs if the prediction engine encounters a system error (e.g. missing serialized model binaries or scaling pipeline failures).
* **Response Content:**
  ```json
  {
    "status": "Internal Server Error",
    "message": "Prediction engine failure: Failed to load model/scaler or perform prediction: ...",
    "model-name": "LogisticRegression",
    "output": {
      "model_id": 1,
      "prediction": "null"
    }
  }
  ```

---

## Setup & Run Instructions

### 1. Set Up Virtual Environment & Dependencies
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py migrate
```

### 3. Start the Django Server
```bash
python manage.py runserver
```
The application will run locally at `http://127.0.0.1:8000/`.
