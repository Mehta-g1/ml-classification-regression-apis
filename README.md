# Django Machine Learning API Project

A production-ready Django web application providing REST APIs to run predictions for five different datasets (Classification and Regression) using pre-trained Machine Learning models. The application supports a unified input interface, accepting both **JSON payloads** (`application/json`) and **Form-Data** / **URL-Encoded** payloads, backed by fast-fail input validation.

---

## Project Structure & Files

Here is the complete project directory structure with explanations of the primary components:

```text
ML Project/
│
├── APIs/                       # Django application package for API views & logic
│   ├── predictor.py            # Contains ML prediction wrappers that load pickled scalers and models
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
│       ├── Automobile/         # auto_price.csv
│       ├── California Housing/ # california_housing.csv
│       └── Concrete Data/      # Concrete_Data.xls
│
├── ML/                         # Project settings package
│   ├── settings.py             # Global Django configurations, middleware, and installed apps
│   ├── urls.py                 # Root URL router (routes /predict/* to APIs.urls)
│   ├── wsgi.py / asgi.py       # WSGI/ASGI gateways for deployment servers
│   └── __init__.py
│
├── ML_models and scalers/      # Binary serialized model pipelines (.pkl format)
│   ├── ML_Models/
│   │   ├── Auto Price/         # Pickled regressors (Linear Regression, Ridge, kNN, Tree, SVR)
│   │   ├── California_Housing/ # Pickled regressors (Linear Regression, Ridge, kNN, Tree, SVR)
│   │   ├── Concrete/           # Pickled regressors (Linear Regression, Ridge, kNN, Tree, SVR)
│   │   ├── Diabetes/           # Pickled classifiers (Logistic Regression, kNN, Decision Tree, SVC)
│   │   └── Heart/              # Pickled classifiers (Logistic Regression, kNN, Decision Tree, SVC)
│   └── Scalers/                # Scikit-learn StandardScaler/preprocessing pipelines
│       ├── auto_scaler.pkl
│       ├── california_housing.pkl
│       ├── concrete_scaler.pkl
│       ├── diabetes_scaler.pkl
│       └── heart_scaler.pkl
│
├── Notebooks/                  # Research, modeling, and training notebooks
│   ├── Classification/
│   │   ├── diabetes.ipynb      # Training & evaluation of classification models for Diabetes
│   │   └── heart.ipynb         # Training & evaluation of classification models for Heart Disease
│   └── Regression/
│       ├── auto_price.ipynb    # Model training and exploratory analysis for auto pricing
│       ├── california_housing.ipynb # Training & evaluation of regression models for housing price index
│       └── concrete.ipynb      # Training & evaluation of regression models for concrete strength
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

### Regression (California Housing, Concrete Strength, Automobile Price Prediction)
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
     "model-name": "LinearRegression",
     ...
   }
   ```
2. **Form-Data / URL-Encoded** (`Content-Type: application/x-www-form-urlencoded` or `multipart/form-data`):
   Key-value pairs sent in the POST request body.

> [!NOTE]
> All endpoints are restricted to the `POST` method. Any `GET` requests will automatically return `405 Method Not Allowed`.

---

## API Documentation & Guides

For a comprehensive guide on sending requests, dataset columns description, parameters, input examples, error messages, and responses for each individual endpoint, please check the **[API Integration & Guidance Manual (API docs.md)](file:///e:/ML%20Project/API%20docs.md)**.

---

## Setup & Run Instructions

### 1. Clone the Repository
```bash
# Clone the project code
git clone https://github.com/Mehta-g1/ml-classification-regression-apis.git
cd ml-classification-regression-apis
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Start the Django Server
```bash
python manage.py runserver
```
The application will run locally at `http://127.0.0.1:8000/`.
