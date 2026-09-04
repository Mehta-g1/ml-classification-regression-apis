# Django Machine Learning API Project

A production-ready Django web application providing RESTful APIs to run real-time inference across 5 distinct Machine Learning datasets (Classification & Regression). The service includes automated preprocessing pipelines, model performance benchmarks, realistic test sample datasets, fast-fail input validations, and built-in CORS support for modern frontend integration.

---

## Project Structure & Architecture

```text
ML Project/
│
├── APIs/                       # Core Django application for ML inference & utilities
│   ├── predictor.py            # Model loading, scaler pipeline execution, and performance scores
│   ├── samples.py              # Authentic test sample dataset extraction with safe fallbacks
│   ├── middleware.py           # Custom CORS middleware with OPTIONS preflight handling
│   ├── views.py                # Prediction and query endpoints with dual-payload parsing
│   ├── urls.py                 # Endpoint URL routes (/predict/*)
│   ├── apps.py                 # Django app configuration
│   └── models.py               # Stateless architecture (database models unused)
│
├── Datasets/                   # Training & sample datasets
│   ├── Classification datasets/
│   │   ├── Diabetes/           # diabetes_dataset.csv
│   │   └── Heart Disease/      # heart.csv
│   └── Regression datasets/
│       ├── Automobile/         # auto_price.csv
│       ├── California Housing/ # california_housing.csv
│       └── Concrete Data/      # Concrete_Data.xls, concrete_data.csv
│
├── ML/                         # Django project configuration
│   ├── settings.py             # Environment configuration, middleware, CORS, Whitenoise
│   ├── urls.py                 # Root URL router
│   ├── wsgi.py / asgi.py       # WSGI/ASGI gateways for deployment (Gunicorn / Render)
│   └── __init__.py
│
├── ML_models and scalers/      # Binary serialized scikit-learn model pipelines (.pkl)
│   ├── ML_Models/              # Trained models grouped by dataset
│   │   ├── Auto Price/         # Linear Regression, Ridge, kNN, Decision Tree, SVR
│   │   ├── California_Housing/ # Linear Regression, Ridge, kNN, Decision Tree, SVR
│   │   ├── Concrete/           # Linear Regression, Ridge, kNN, Decision Tree, SVR
│   │   ├── Diabetes/           # Logistic Regression, kNN, Decision Tree, SVC
│   │   └── Heart/              # Logistic Regression, kNN, Decision Tree, SVC
│   └── Scalers/                # Scikit-learn StandardScaler/preprocessors (.pkl)
│       ├── auto_scaler.pkl
│       ├── california_housing.pkl
│       ├── concrete_scaler.pkl
│       ├── diabetes_scaler.pkl
│       └── heart_scaler.pkl
│
├── Notebooks/                  # Exploratory data analysis, training & evaluation notebooks
│   ├── Classification/         # heart.ipynb, diabetes.ipynb
│   └── Regression/             # auto_price.ipynb, california_housing.ipynb, concrete.ipynb
│
├── build.sh                    # Deployment build script for cloud hosting (Render)
├── manage.py                   # Django CLI administrative entry point
└── requirements.txt            # Python dependencies (Django, scikit-learn, pandas, etc.)
```

---

## Supported Machine Learning Models

### Classification Tasks (Heart Disease, Diabetes Risk)
| Model ID | Model Name | Description |
| :--- | :--- | :--- |
| `1` | `LogisticRegression` | Linear classification baseline |
| `2` | `KNeighborsClassifier` | Non-parametric proximity-based classification |
| `3` | `DecisionTreeClassifier` | Tree-structured rule-based classifier |
| `4` | `SVC` | Support Vector Classifier with non-linear RBF kernel |

### Regression Tasks (California Housing, Concrete Strength, Auto Price)
| Model ID | Model Name | Description |
| :--- | :--- | :--- |
| `1` | `LinearRegression` | Ordinary least squares regression baseline |
| `2` | `Ridge` | L2-regularized linear regression |
| `3` | `KNeighborsRegressor` | Distance-weighted continuous output regression |
| `4` | `DecisionTreeRegressor` | Multi-split recursive regression tree |
| `5` | `SVR` | Epsilon-Support Vector Regression |

---

## API Capabilities

1. **Prediction Endpoints (`POST`)**:
   - `/predict/heart/` - Heart disease risk assessment
   - `/predict/diabetes/` - Diabetes diagnosis prediction
   - `/predict/california-housing/` - Median house value estimation
   - `/predict/concrete/` - Concrete compressive strength prediction
   - `/predict/auto-price/` - Automobile market price forecast

2. **Benchmark & Accuracy Metrics (`GET`)**:
   - `/predict/accuracy/` - Full benchmark metrics across all datasets and models (filtered via `?dataset=heart | diabetes | california-housing | concrete | auto-price`).

3. **Authentic Test Samples (`GET`)**:
   - `/predict/samples/` - Test sample records with actual ground-truth values (filtered via `?dataset=...`).

4. **Payload Flexibility**:
   - Accepts both **JSON** (`application/json`) and **Form-Data / URL-Encoded** bodies seamlessly.
   - Built-in CORS preflight (`OPTIONS`) handling for modern single-page applications.

---

## API Documentation

For the complete API manual with feature dictionaries, sample payloads, query parameters, status codes, and error responses, check **[API docs.md](file:///e:/ML%20Project/API%20docs.md)**.

---

## Setup & Local Run Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Mehta-g1/ml-classification-regression-apis.git
cd ml-classification-regression-apis
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create and activate virtual environment (Windows)
python -m venv .venv
.\.venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-custom-django-secret-key
```

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

The Django API service will be accessible locally at `http://127.0.0.1:8000/`.
