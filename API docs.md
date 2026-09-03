# Developer API Guide

Hey! Here is a quick, human-friendly guide to querying our ML prediction APIs.

---

## 1. Quick Integration Tips

* **Flexible Formats:** We support both JSON (`application/json`) and Form-Data/URL-Encoded bodies. The server handles parsing automatically.
* **POST Only:** All endpoints require `POST` requests. `GET` requests will fail with a `405 Method Not Allowed`.
* **Trailing Slash:** You **must** append a `/` to the URLs (e.g. `/predict/auto-price/`) or Django's redirect might break your request.

---

## 2. API Endpoints

### 1. Automobile Price Prediction
* **URL:** `/predict/auto-price/`
* **Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`
* **Features:** `horsepower`, `curb-weight`, `engine-size`, `highway-mpg`, `city-mpg`, `wheel-base`, `length`, `width` (all floats).
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "LinearRegression",
    "horsepower": 111.0,
    "curb-weight": 2548.0,
    "engine-size": 130.0,
    "highway-mpg": 27.0,
    "city-mpg": 21.0,
    "wheel-base": 88.6,
    "length": 168.8,
    "width": 64.1
  }
  ```
* **Response Output:** Returns the estimated car price in USD (`Prediction`) and the model metrics.

### 2. Concrete Compressive Strength
* **URL:** `/predict/concrete/`
* **Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`
* **Features:** `cement`, `slag`, `fly_ash`, `water`, `superplasticizer`, `coarse_aggregate`, `fine_aggregate`, `age` (all floats).
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "LinearRegression",
    "cement": 540.0,
    "slag": 0.0,
    "fly_ash": 0.0,
    "water": 162.0,
    "superplasticizer": 2.5,
    "coarse_aggregate": 1040.0,
    "fine_aggregate": 676.0,
    "age": 28.0
  }
  ```
* **Response Output:** Returns the predicted strength in Megapascals (`Prediction`) and the model metrics.

### 3. California Housing Prices
* **URL:** `/predict/california-housing/`
* **Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`
* **Features:** `MedInc`, `HouseAge`, `AveRooms`, `AveBedrms`, `Population`, `AveOccup`, `Latitude`, `Longitude` (all floats).
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "LinearRegression",
    "MedInc": 8.32,
    "HouseAge": 41.0,
    "AveRooms": 6.98,
    "AveBedrms": 1.02,
    "Population": 322.0,
    "AveOccup": 2.55,
    "Latitude": 37.88,
    "Longitude": -122.23
  }
  ```
* **Response Output:** Returns the median block value in hundreds of thousands of USD (`Prediction`).

### 4. Diabetes Risk Classification
* **URL:** `/predict/diabetes/`
* **Models:** `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `SVC`
* **Features:** `age`, `bmi`, `glucose_fasting`, `hba1c`, `physical_activity_minutes_per_week`, `cardiovascular_history` (floats); `family_history_diabetes`, `hypertension_history` (`"1"` or `"0"`); `gender` (`"Male"`, `"Female"`, `"Other"`); `smoking_status` (`"Never"`, `"Former"`, `"Current"`).
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "LogisticRegression",
    "age": 58,
    "bmi": 30.0,
    "family_history_diabetes": "0",
    "hypertension_history": "0",
    "glucose_fasting": 136,
    "hba1c": 8.18,
    "physical_activity_minutes_per_week": 215,
    "cardiovascular_history": "0",
    "gender": "Male",
    "smoking_status": "Never"
  }
  ```
* **Response Output:** Returns risk classification (`Prediction`: `1` for risk, `0` otherwise).

### 5. Heart Disease Classification
* **URL:** `/predict/heart/`
* **Models:** `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `SVC`
* **Features:** `age`, `sex` (`1`=M, `0`=F), `cp` (chest pain `0`-`3`), `trestbps`, `chol`, `fbs` (`1` or `0`), `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal` (all floats).
* **Sample Request (JSON):**
  ```json
  {
    "model-name": "LogisticRegression",
    "age": 52,
    "sex": 0,
    "cp": 2,
    "trestbps": 136,
    "chol": 196,
    "fbs": 0,
    "restecg": 0,
    "thalach": 169,
    "exang": 0,
    "oldpeak": 0.1,
    "slope": 1,
    "ca": 0,
    "thal": 2
  }
  ```
* **Response Output:** Returns heart disease classification (`Prediction`: `1` or `0`).

---

## 3. Sample Response Format (200 OK)

All APIs return a standard success response containing the prediction result and model accuracy metrics:
```json
{
  "status": "Ok",
  "message": "Success",
  "model-name": "LinearRegression",
  "output": {
    "Prediction": 13495.0,
    "model-accuracy": {
      "r2_score": 0.799,
      "mean_absolute_error": 2815.49,
      "mean_squared_error": 15659145.59
    }
  }
}
```

---

## 4. Handling Error Responses

When something goes wrong, the API outputs a clean JSON response rather than letting the server crash:

* **`400 Bad Request`**
  * **Invalid JSON:** Your JSON payload is broken (missing commas, quotes, etc.).
  * **Missing / Wrong Model Name:** Ensure `"model-name"` is provided and is one of the supported models.
  * **Sample Response:**
    ```json
    {
      "status": "Bad Request",
      "message": "Missing required field: 'model-name'.",
      "output": {
        "model_id": null,
        "prediction": "null"
      }
    }
    ```

* **`422 Unprocessable Content`**
  * **Missing parameters or non-numeric types:** You missed a field or passed text where a number belongs.
  * **Sample Response:**
    ```json
    {
      "status": "Unprocessable Entity",
      "message": "Input validation failed.",
      "errors": [
        "Field 'horsepower' is required."
      ],
      "model-name": "LinearRegression",
      "output": {
        "model_id": 1,
        "prediction": "null"
      }
    }
    ```

* **`500 Internal Server Error`**
  * **System Error:** The server couldn't load the model file. Check Django terminal logs for the traceback.
