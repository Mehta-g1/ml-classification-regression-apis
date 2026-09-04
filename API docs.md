# Developer API Reference Guide

Welcome to the Machine Learning API documentation. This guide details how to query the prediction engines, fetch live model accuracy scores, load test samples, and handle server responses.

---

## 1. Quick Integration Rules

* **Base URL:**
  * Local Development: `http://127.0.0.1:8000`
  * Production: `https://ml-apis-lqlt.onrender.com`
* **Request Headers:**
  * Predictions (`POST`): `Content-Type: application/json` or `application/x-www-form-urlencoded`
  * Info & Samples (`GET`): `Accept: application/json`
* **Trailing Slashes:** Always include trailing slashes on endpoints (e.g. `/predict/heart/`, `/predict/accuracy/`).
* **CORS:** Built-in CORS middleware handles preflight `OPTIONS` requests automatically.

---

## 2. Model Accuracy & Benchmark Endpoint

### `GET /predict/accuracy/`
Fetches model performance metrics across all models and datasets.

* **Query Parameters (Optional):**
  * `?dataset=heart` | `diabetes` | `california-housing` | `concrete` | `auto-price`
* **Sample Request:**
  ```http
  GET /predict/accuracy/?dataset=heart HTTP/1.1
  Host: 127.0.0.1:8000
  ```
* **Sample Response (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Accuracy metrics retrieved successfully",
    "dataset": "heart",
    "data": {
      "dataset_id": "heart",
      "name": "Heart Disease Risk",
      "dataset_name": "Heart Disease Classification",
      "type": "classification",
      "target": "Heart Disease (0 = No Disease, 1 = Disease)",
      "best_model": "KNeighborsClassifier",
      "models": [
        {
          "model_id": 1,
          "model_code": 1,
          "model_name": "LogisticRegression",
          "metrics": {
            "accuracy_score": 0.7763,
            "recall_score": 0.8889,
            "f1_score": 0.7901
          },
          "is_best": false
        },
        {
          "model_id": 2,
          "model_code": 2,
          "model_name": "KNeighborsClassifier",
          "metrics": {
            "accuracy_score": 0.7895,
            "recall_score": 0.9444,
            "f1_score": 0.8095
          },
          "is_best": true
        }
      ]
    }
  }
  ```

---

## 3. Dataset Test Samples Endpoint

### `GET /predict/samples/`
Fetches verified test sample records directly from dataset files with ground-truth values for quick testing.

* **Query Parameters (Optional):**
  * `?dataset=heart` | `diabetes` | `california-housing` | `concrete` | `auto-price`
* **Sample Request:**
  ```http
  GET /predict/samples/?dataset=concrete HTTP/1.1
  Host: 127.0.0.1:8000
  ```
* **Sample Response (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Sample test records retrieved successfully",
    "dataset": "concrete",
    "data": {
      "dataset_id": "concrete",
      "name": "Concrete Compressive Strength",
      "samples": [
        {
          "id": "concrete-sample-1",
          "row_index": 1,
          "title": "Concrete Mixture Batch #1 (High Strength)",
          "description": "Cement: 540.0 kg/m³, Water: 162.0 kg/m³, Curing Age: 28 days.",
          "actual_target": 79.99,
          "ground_truth": "79.99 MPa Compressive Strength",
          "data": {
            "cement": 540.0,
            "slag": 0.0,
            "fly_ash": 0.0,
            "water": 162.0,
            "superplasticizer": 2.5,
            "coarse_aggregate": 1040.0,
            "fine_aggregate": 676.0,
            "age": 28.0
          }
        }
      ]
    }
  }
  ```

---

## 4. Prediction Endpoints

### 1. Heart Disease Classification
* **Endpoint:** `POST /predict/heart/`
* **Supported Models:** `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `SVC`
* **Features:**
  * `model-name` *(string, required)*
  * `age` *(float)*, `sex` *(1 = Male, 0 = Female)*, `cp` *(chest pain 0-3)*, `trestbps` *(resting blood pressure)*
  * `chol` *(serum cholesterol)*, `fbs` *(fasting blood sugar > 120 mg/dl: 1 or 0)*, `restecg` *(resting ECG 0-2)*
  * `thalach` *(max heart rate)*, `exang` *(exercise angina: 1 or 0)*, `oldpeak` *(ST depression)*
  * `slope` *(slope of peak ST segment 0-2)*, `ca` *(major vessels colored by fluoroscopy 0-3)*, `thal` *(thalassemia 1-3)*
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "LogisticRegression",
    "age": 55,
    "sex": 1,
    "cp": 0,
    "trestbps": 140,
    "chol": 240,
    "fbs": 0,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 1.2,
    "slope": 1,
    "ca": 0,
    "thal": 2
  }
  ```
* **Sample Response (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "LogisticRegression",
    "output": {
      "Prediction": 0,
      "model-accuracy": {
        "accuracy_score": 0.7763,
        "recall_score": 0.8889,
        "f1_score": 0.7901
      }
    }
  }
  ```

---

### 2. Diabetes Risk Prediction
* **Endpoint:** `POST /predict/diabetes/`
* **Supported Models:** `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `SVC`
* **Features:**
  * `model-name` *(string, required)*
  * `age` *(float)*, `bmi` *(float)*, `glucose_fasting` *(float)*, `hba1c` *(float)*
  * `physical_activity_minutes_per_week` *(float)*, `cardiovascular_history` *(0 or 1)*
  * `family_history_diabetes` *(string: "1" or "0")*, `hypertension_history` *(string: "1" or "0")*
  * `gender` *(string: "Male", "Female", or "Other")*, `smoking_status` *(string: "Never", "Former", or "Current")*
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "DecisionTreeClassifier",
    "age": 45,
    "bmi": 28.5,
    "glucose_fasting": 110,
    "hba1c": 5.8,
    "physical_activity_minutes_per_week": 150,
    "cardiovascular_history": 0,
    "family_history_diabetes": "1",
    "hypertension_history": "0",
    "gender": "Male",
    "smoking_status": "Never"
  }
  ```
* **Sample Response (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "DecisionTreeClassifier",
    "output": {
      "Prediction": 1,
      "model-accuracy": {
        "accuracy_score": 0.9204,
        "recall_score": 0.867,
        "f1_score": 0.9288
      }
    }
  }
  ```

---

### 3. California Housing Price Regression
* **Endpoint:** `POST /predict/california-housing/`
* **Supported Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`
* **Features:**
  * `model-name` *(string, required)*
  * `MedInc` *(median income in block, tens of thousands)*, `HouseAge` *(median house age in years)*
  * `AveRooms` *(average rooms per household)*, `AveBedrms` *(average bedrooms per household)*
  * `Population` *(block population)*, `AveOccup` *(average occupancy per household)*
  * `Latitude` *(latitude float)*, `Longitude` *(longitude float)*
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "SVR",
    "MedInc": 3.5,
    "HouseAge": 25,
    "AveRooms": 5.2,
    "AveBedrms": 1.1,
    "Population": 1200,
    "AveOccup": 3.1,
    "Latitude": 34.2,
    "Longitude": -118.4
  }
  ```
* **Sample Response (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "SVR",
    "output": {
      "Prediction": 1.9964,
      "model-accuracy": {
        "r2_score": 0.7416,
        "mean_absolute_error": 0.3924,
        "mean_squared_error": 0.3526
      }
    }
  }
  ```

---

### 4. Concrete Compressive Strength Prediction
* **Endpoint:** `POST /predict/concrete/`
* **Supported Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`
* **Features:**
  * `model-name` *(string, required)*
  * `cement` *(kg/m³)*, `slag` *(blast furnace slag, kg/m³)*, `fly_ash` *(kg/m³)*
  * `water` *(kg/m³)*, `superplasticizer` *(kg/m³)*, `coarse_aggregate` *(kg/m³)*
  * `fine_aggregate` *(sand, kg/m³)*, `age` *(curing age in days)*
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "SVR",
    "cement": 250.0,
    "slag": 100.0,
    "fly_ash": 50.0,
    "water": 180.0,
    "superplasticizer": 2.5,
    "coarse_aggregate": 900.0,
    "fine_aggregate": 750.0,
    "age": 28.0
  }
  ```
* **Sample Response (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "SVR",
    "output": {
      "Prediction": 29.28,
      "model-accuracy": {
        "r2_score": 0.8867,
        "mean_absolute_error": 3.9354,
        "mean_squared_error": 30.7083
      }
    }
  }
  ```

---

### 5. Automobile Price Prediction
* **Endpoint:** `POST /predict/auto-price/`
* **Supported Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`
* **Features:**
  * `model-name` *(string, required)*
  * `horsepower` *(hp)*, `curb-weight` *(lbs)*, `engine-size` *(cubic inches)*
  * `highway-mpg` *(mpg)*, `city-mpg` *(mpg)*, `wheel-base` *(inches)*
  * `length` *(inches)*, `width` *(inches)*
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "DecisionTreeRegressor",
    "horsepower": 110.0,
    "curb-weight": 2500.0,
    "engine-size": 130.0,
    "highway-mpg": 30.0,
    "city-mpg": 24.0,
    "wheel-base": 98.8,
    "length": 175.5,
    "width": 65.5
  }
  ```
* **Sample Response (200 OK):**
  ```json
  {
    "status": "Ok",
    "message": "Success",
    "model-name": "DecisionTreeRegressor",
    "output": {
      "Prediction": 13381.34,
      "model-accuracy": {
        "r2_score": 0.9246,
        "mean_absolute_error": 1712.8521,
        "mean_squared_error": 5877138.0836
      }
    }
  }
  ```

---

## 5. Error Handling & HTTP Status Codes

The API always returns structured JSON payloads for errors:

| Status Code | Type | Meaning & Action |
| :--- | :--- | :--- |
| `200 OK` | Success | Inference succeeded; output payload contains numeric prediction and accuracy scores. |
| `400 Bad Request` | Client Error | Malformed JSON body, missing `"model-name"`, or invalid model name specified. |
| `405 Method Not Allowed` | Routing Error | HTTP method was not `POST` for predictions or `GET` for benchmarks/samples. |
| `422 Unprocessable Entity` | Validation Error | One or more required feature fields are missing or non-numeric. Check the `errors` array. |
| `500 Internal Server Error` | Engine Error | Exception inside prediction runtime / scaler transformation. |

### Example 422 Validation Error:
```json
{
  "status": "Unprocessable Entity",
  "message": "Input validation failed. Please check the errors field for details.",
  "errors": [
    "Field 'horsepower' is required.",
    "Field 'engine-size' must be numeric (received: 'abc')."
  ],
  "model-name": "LinearRegression",
  "output": {
    "model_id": 1,
    "prediction": "null"
  }
}
```
