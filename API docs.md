# API Integration & Guidance Manual

Welcome! This documentation guide is designed to help you integrate and interact with our Django-based Machine Learning inference APIs. 

Our system serves predictions for both **classification** tasks (Heart Disease & Diabetes) and **regression** tasks (California Housing prices & Concrete Compressive Strength) using various machine learning model architectures. 

---

## 1. Core Architecture & Design Philosophy

To prevent server crashes and support modern client integrations, the API layer is built with three main design patterns:

1. **Payload Flexibility:**
   The backend automatically detects the request payload content type. Whether your application sends standard JSON payloads (`application/json`) from a frontend framework or Form-Data / URL-Encoded pairs (`multipart/form-data`) from client tools like Postman, the API extracts the parameters seamlessly.
2. **Fast-Fail Input Validation:**
   Before a machine learning model is loaded, the request data is passed through a strict validator. If fields are missing, empty, or cannot be parsed into numbers, the API rejects the request immediately with an HTTP `422 Unprocessable Entity` status. This prevents malformed data from ever reaching the modeling layer.
3. **Safe Exception Boundaries:**
   If a model file is missing or the inference code runs into a calculation error, the exception is caught within the request lifecycle. The API responds with a structured HTTP `500 Internal Server Error` JSON payload rather than crashing Django's thread loop.

---

## 2. API Endpoints Reference

> [!IMPORTANT]
> **Trailing Slash Rule:** All endpoints require a trailing slash (`/`). If you send a request without a trailing slash (e.g. `/predict/concrete`), Django's common middleware will issue a `301 Redirect` which might convert your `POST` request into a `GET` request and cause a `405 Method Not Allowed` error. Always append the `/` at the end of the URL path!

---

### Endpoint A: Predict Concrete Compressive Strength
Predicts the compressive strength of high-performance concrete mixtures (in Megapascals, MPa) based on material ingredients and aging characteristics.

* **URL:** `/predict/concrete/`
* **Method:** `POST`
* **Supported Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`

#### Input Parameters Guide
| Parameter | Type | Required | Description / Unit | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `model-name` | String | Yes | Name of the ML model architecture to use | `LinearRegression` |
| `cement` | Float | Yes | Cement content (kg in a m³ mixture) | `540.0` |
| `slag` | Float | Yes | Blast furnace slag content (kg in a m³ mixture) | `0.0` |
| `fly_ash` | Float | Yes | Fly ash content (kg in a m³ mixture) | `0.0` |
| `water` | Float | Yes | Water content (kg in a m³ mixture) | `162.0` |
| `superplasticizer` | Float | Yes | Superplasticizer content (kg in a m³ mixture) | `2.5` |
| `coarse_aggregate`| Float | Yes | Coarse aggregate content (kg in a m³ mixture) | `1040.0` |
| `fine_aggregate` | Float | Yes | Fine aggregate content (kg in a m³ mixture) | `676.0` |
| `age` | Float | Yes | Age of curing in days (usually `28`) | `28` |

#### Request Example (JSON Payload)
```json
{
  "model-name": "LinearRegression",
  "cement": "540.0",
  "slag": "0.0",
  "fly_ash": "0.0",
  "water": "162.0",
  "superplasticizer": "2.5",
  "coarse_aggregate": "1040.0",
  "fine_aggregate": "676.0",
  "age": "28"
}
```

#### Successful Response Output (`200 OK`)
```json
{
  "status": "Ok",
  "message": "Success",
  "model-name": "LinearRegression",
  "output": {
    "Prediction": 79.986111,
    "model-accuracy": {
      "r2_score": 0.6128899126006704,
      "mean_absolute_error": 8.186575235450505,
      "mean_squared_error": 104.92832620839133
    }
  }
}
```

---

### Endpoint B: Predict California Housing Prices
Estimates the median house value of California districts (represented in hundreds of thousands of dollars, e.g., `4.12` represents `$412,000`).

* **URL:** `/predict/california-housing/`
* **Method:** `POST`
* **Supported Models:** `LinearRegression`, `Ridge`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `SVR`

#### Input Parameters Guide
| Parameter | Type | Required | Description / Unit | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `model-name` | String | Yes | Name of the ML model architecture to use | `LinearRegression` |
| `MedInc` | Float | Yes | Median income in block group (in tens of thousands of USD) | `8.3252` |
| `HouseAge` | Float | Yes | Median house age in the block group | `41.0` |
| `AveRooms` | Float | Yes | Average number of rooms per household | `6.984127` |
| `AveBedrms` | Float | Yes | Average number of bedrooms per household | `1.023810` |
| `Population` | Float | Yes | Block group population | `322.0` |
| `AveOccup` | Float | Yes | Average household occupancy (people per house) | `2.555556` |
| `Latitude` | Float | Yes | Block group latitude coordinates | `37.88` |
| `Longitude` | Float | Yes | Block group longitude coordinates | `-122.23` |

#### Request Example (JSON Payload)
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

#### Successful Response Output (`200 OK`)
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

### Endpoint C: Predict Diabetes
Evaluates a patient's indicators to determine whether they are likely to have diabetes (`1` = positive, `0` = negative).

* **URL:** `/predict/diabetes/`
* **Method:** `POST`
* **Supported Models:** `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `SVC`

#### Input Parameters Guide
| Parameter | Type | Required | Description / Range | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `model-name` | String | Yes | Name of the ML classification model to use | `LogisticRegression` |
| `age` | Float | Yes | Patient age in years | `58` |
| `bmi` | Float | Yes | Body Mass Index (BMI) of the patient | `30.0` |
| `family_history_diabetes` | String | Yes | Family history of diabetes (`'1'` for Yes, `'0'` for No) | `0` |
| `hypertension_history` | String | Yes | History of hypertension/high BP (`'1'` for Yes, `'0'` for No) | `0` |
| `glucose_fasting` | Float | Yes | Fasting glucose level | `136` |
| `hba1c` | Float | Yes | HbA1c blood test percentage score | `8.18` |
| `physical_activity_minutes_per_week`| Float | Yes | Physical activity time in minutes per week | `215` |
| `cardiovascular_history`| String | Yes | History of cardiovascular disease (`'1'` for Yes, `'0'` for No) | `0` |
| `gender` | String | Yes | Biological gender (`Male`, `Female`, `Other`) | `Male` |
| `smoking_status` | String | Yes | Smoking habits status (`Never`, `Former`, `Current`) | `Never` |

#### Request Example (JSON Payload)
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

#### Successful Response Output (`200 OK`)
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

### Endpoint D: Predict Heart Disease
Evaluates cardiovascular test metrics to classify presence of heart disease (`1` = positive, `0` = negative).

* **URL:** `/predict/heart/`
* **Method:** `POST`
* **Supported Models:** `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `SVC`

#### Input Parameters Guide
| Parameter | Type | Required | Description / Valid Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `model-name` | String | Yes | Name of the ML classification model to use | `LogisticRegression` |
| `age` | Float | Yes | Patient age in years | `52` |
| `sex` | Float | Yes | Sex (`1` = Male, `0` = Female) | `0` |
| `cp` | Float | Yes | Chest pain type (`0` = asymptomatic, `1`, `2`, `3`) | `2` |
| `trestbps` | Float | Yes | Resting blood pressure in mm Hg | `136` |
| `chol` | Float | Yes | Serum cholestoral in mg/dl | `196` |
| `fbs` | Float | Yes | Fasting blood sugar > 120 mg/dl (`1` = true, `0` = false) | `0` |
| `restecg` | Float | Yes | Resting electrocardiographic results (`0`, `1`, `2`) | `0` |
| `thalach` | Float | Yes | Maximum heart rate achieved | `169` |
| `exang` | Float | Yes | Exercise induced angina (`1` = Yes, `0` = No) | `0` |
| `oldpeak` | Float | Yes | ST depression induced by exercise relative to rest | `0.1` |
| `slope` | Float | Yes | Slope of peak exercise ST segment (`0`, `1`, `2`) | `1` |
| `ca` | Float | Yes | Number of major vessels colored by fluoroscopy (`0`-`4`) | `0` |
| `thal` | Float | Yes | Thalassemia status (`0` = normal, `1` = fixed, `2` = reversible) | `2` |

#### Request Example (JSON Payload)
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

#### Successful Response Output (`200 OK`)
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

## 3. Explaining Errors and Troubleshooting

When something goes wrong, the APIs do not throw raw server crashes. Instead, you will receive structured HTTP status responses detailing exactly what happened and how to address it.

### HTTP `400 Bad Request`
This error occurs if your payload is structurally broken or requests a model that does not exist.

* **Scenario A: Missing or Invalid JSON syntax**
  * *What it means:* The server failed to parse your JSON body because of a missing comma, unclosed quotes, or bad formatting.
  * *Response:*
    ```json
    {
      "status": "Bad Request",
      "message": "Invalid JSON format in request body.",
      "output": { "model_id": null, "prediction": "null" }
    }
    ```
  * *How to resolve:* Double-check your JSON syntax with a validator (e.g., JSONLint) and ensure you are sending the `Content-Type: application/json` header.
  
* **Scenario B: Missing `model-name` parameter**
  * *What it means:* The request did not include the `model-name` parameter, which is required to route the query to the correct pickeled model.
  * *Response:*
    ```json
    {
      "status": "Bad Request",
      "message": "Missing required field: 'model-name'.",
      "output": { "model_id": null, "prediction": "null" }
    }
    ```
  * *How to resolve:* Add `"model-name": "LinearRegression"` (or another supported model) to your request parameters.

* **Scenario C: Incorrect or Unsupported model name**
  * *What it means:* You provided a model name that the system does not recognize.
  * *Response:*
    ```json
    {
      "status": "Bad Request",
      "message": "Wrong Model Name: 'MyCustomModel'. Available options: ['LinearRegression', 'Ridge', 'KNeighborsRegressor', 'DecisionTreeRegressor', 'SVR']",
      "model-name": "MyCustomModel",
      "output": { "model_id": null, "prediction": "null" }
    }
    ```
  * *How to resolve:* Replace your model name with one of the recommended options listed in the error message. Note that classification endpoints use classification models, and regression endpoints use regression models.

---

### HTTP `422 Unprocessable Entity`
This error occurs when the server parsed your request successfully, but the values you supplied failed validation rules.

* **Scenario A: Missing features**
  * *What it means:* You missed one or more required input parameters that the ML model needs for calculation.
  * *Response:*
    ```json
    {
      "status": "Unprocessable Entity",
      "message": "Input validation failed. Please check the errors field for details.",
      "errors": [ "Field 'cement' is required." ],
      "model-name": "LinearRegression",
      "output": { "model_id": 1, "prediction": "null" }
    }
    ```
  * *How to resolve:* Check the `errors` array in the response and append the missing keys to your request body.

* **Scenario B: Non-numeric inputs**
  * *What it means:* You sent string text (e.g., `"five hundred"`) instead of a valid number for a clinical or material field.
  * *Response:*
    ```json
    {
      "status": "Unprocessable Entity",
      "message": "Input validation failed. Please check the errors field for details.",
      "errors": [ "Field 'water' must be numeric (received: 'none')." ],
      "model-name": "LinearRegression",
      "output": { "model_id": 1, "prediction": "null" }
    }
    ```
  * *How to resolve:* Convert the parameter value in your client code to a numeric integer or decimal string (e.g., `"162.0"` or `162.0`).

---

### HTTP `405 Method Not Allowed`
* *What it means:* You attempted to query the endpoint using `GET`, `PUT`, `DELETE`, or another method. The prediction engine is write-only and only accepts `POST` transactions.
* *Response:* A standard Django 405 error page.
* *How to resolve:* Ensure your integration utility (e.g., Axios, Fetch, Postman, cURL) is configured to send a `POST` request.

---

### HTTP `500 Internal Server Error`
* *What it means:* The server encountered a system configuration error. This usually indicates that the pickeled `.pkl` model file or the scaler file is missing from the directory, or contains structure mismatches.
* *Response:*
  ```json
  {
    "status": "Internal Server Error",
    "message": "Prediction engine failure: Failed to load model/scaler or perform prediction: ...",
    "model-name": "LinearRegression",
    "output": { "model_id": 1, "prediction": "null" }
  }
  ```
* *How to resolve:* Check your terminal console logs to inspect the error log. Ensure all picker files exist in `ML_models and scalers/ML_Models/*` and that your inputs match the training features.
