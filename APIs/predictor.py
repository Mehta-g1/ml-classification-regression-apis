import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'ML_models and scalers'

CLASSIFIER_PREDICTOR_MODEL_CODE = {
    'LogisticRegression': 1,
    'KNeighborsClassifier': 2,
    'DecisionTreeClassifier': 3,
    'SVC': 4
}

CLASSIFIER_CODE_TO_NAME = {v: k for k, v in CLASSIFIER_PREDICTOR_MODEL_CODE.items()}

REGRESSOR_PREDICTOR_MODEL_CODE = {
    'LinearRegression': 1,
    'Ridge': 2,
    'KNeighborsRegressor': 3,
    'DecisionTreeRegressor': 4,
    'SVR': 5
}

REGRESSOR_CODE_TO_NAME = {v: k for k, v in REGRESSOR_PREDICTOR_MODEL_CODE.items()}

HEART_MODEL_SCORES = {
    1: {'accuracy_score': 0.7763, 'recall_score': 0.8889, 'f1_score': 0.7901},
    2: {'accuracy_score': 0.7895, 'recall_score': 0.9444, 'f1_score': 0.8095},
    3: {'accuracy_score': 0.7763, 'recall_score': 0.8889, 'f1_score': 0.7901},
    4: {'accuracy_score': 0.7500, 'recall_score': 0.8333, 'f1_score': 0.7595}
}

DIABETES_MODEL_SCORES = {
    1: {'accuracy_score': 0.8847, 'recall_score': 0.8176, 'f1_score': 0.8946},
    2: {'accuracy_score': 0.8743, 'recall_score': 0.8622, 'f1_score': 0.8914},
    3: {'accuracy_score': 0.9204, 'recall_score': 0.8670, 'f1_score': 0.9288},
    4: {'accuracy_score': 0.8996, 'recall_score': 0.8714, 'f1_score': 0.9122}
}

CALIFORNIA_HOUSING_SCORES = {
    1: {'r2_score': 0.6010, 'mean_absolute_error': 0.5367, 'mean_squared_error': 0.5445},
    2: {'r2_score': 0.5972, 'mean_absolute_error': 0.5387, 'mean_squared_error': 0.5496},
    3: {'r2_score': 0.7414, 'mean_absolute_error': 0.3961, 'mean_squared_error': 0.3529},
    4: {'r2_score': 0.7277, 'mean_absolute_error': 0.4011, 'mean_squared_error': 0.3715},
    5: {'r2_score': 0.7416, 'mean_absolute_error': 0.3924, 'mean_squared_error': 0.3526}
}

CONCRETE_SCORES = {
    1: {'r2_score': 0.6129, 'mean_absolute_error': 8.1866, 'mean_squared_error': 104.9283},
    2: {'r2_score': 0.6133, 'mean_absolute_error': 8.1868, 'mean_squared_error': 104.8045},
    3: {'r2_score': 0.8030, 'mean_absolute_error': 5.4923, 'mean_squared_error': 53.3949},
    4: {'r2_score': 0.8798, 'mean_absolute_error': 3.7901, 'mean_squared_error': 32.5838},
    5: {'r2_score': 0.8867, 'mean_absolute_error': 3.9354, 'mean_squared_error': 30.7083}
}

AUTO_PRICE_SCORES = {
    1: {'r2_score': 0.7992, 'mean_absolute_error': 2815.4907, 'mean_squared_error': 15659145.5968},
    2: {'r2_score': 0.7754, 'mean_absolute_error': 2994.3329, 'mean_squared_error': 17509085.3138},
    3: {'r2_score': 0.7594, 'mean_absolute_error': 2319.0700, 'mean_squared_error': 18760831.2684},
    4: {'r2_score': 0.9246, 'mean_absolute_error': 1712.8521, 'mean_squared_error': 5877138.0836},
    5: {'r2_score': 0.7589, 'mean_absolute_error': 2984.9476, 'mean_squared_error': 18801163.4203}
}


def get_all_dataset_accuracies(dataset_filter=None):
    datasets_meta = {
        'heart': {
            'dataset_name': 'Heart Disease Classification',
            'task_type': 'classification',
            'target': 'Heart Disease (0 = No Disease, 1 = Disease)',
            'models': [
                {'model_id': 1, 'model_name': 'LogisticRegression', 'metrics': HEART_MODEL_SCORES[1]},
                {'model_id': 2, 'model_name': 'KNeighborsClassifier', 'metrics': HEART_MODEL_SCORES[2]},
                {'model_id': 3, 'model_name': 'DecisionTreeClassifier', 'metrics': HEART_MODEL_SCORES[3]},
                {'model_id': 4, 'model_name': 'SVC', 'metrics': HEART_MODEL_SCORES[4]}
            ]
        },
        'diabetes': {
            'dataset_name': 'Diabetes Risk Classification',
            'task_type': 'classification',
            'target': 'Diabetes Diagnosis (0 = Non-Diabetic, 1 = Diabetic)',
            'models': [
                {'model_id': 1, 'model_name': 'LogisticRegression', 'metrics': DIABETES_MODEL_SCORES[1]},
                {'model_id': 2, 'model_name': 'KNeighborsClassifier', 'metrics': DIABETES_MODEL_SCORES[2]},
                {'model_id': 3, 'model_name': 'DecisionTreeClassifier', 'metrics': DIABETES_MODEL_SCORES[3]},
                {'model_id': 4, 'model_name': 'SVC', 'metrics': DIABETES_MODEL_SCORES[4]}
            ]
        },
        'california-housing': {
            'dataset_name': 'California Housing Price Regression',
            'task_type': 'regression',
            'target': 'Median House Value (in $100,000s)',
            'models': [
                {'model_id': 1, 'model_name': 'LinearRegression', 'metrics': CALIFORNIA_HOUSING_SCORES[1]},
                {'model_id': 2, 'model_name': 'Ridge', 'metrics': CALIFORNIA_HOUSING_SCORES[2]},
                {'model_id': 3, 'model_name': 'KNeighborsRegressor', 'metrics': CALIFORNIA_HOUSING_SCORES[3]},
                {'model_id': 4, 'model_name': 'DecisionTreeRegressor', 'metrics': CALIFORNIA_HOUSING_SCORES[4]},
                {'model_id': 5, 'model_name': 'SVR', 'metrics': CALIFORNIA_HOUSING_SCORES[5]}
            ]
        },
        'concrete': {
            'dataset_name': 'Concrete Compressive Strength Regression',
            'task_type': 'regression',
            'target': 'Compressive Strength (MPa)',
            'models': [
                {'model_id': 1, 'model_name': 'LinearRegression', 'metrics': CONCRETE_SCORES[1]},
                {'model_id': 2, 'model_name': 'Ridge', 'metrics': CONCRETE_SCORES[2]},
                {'model_id': 3, 'model_name': 'KNeighborsRegressor', 'metrics': CONCRETE_SCORES[3]},
                {'model_id': 4, 'model_name': 'DecisionTreeRegressor', 'metrics': CONCRETE_SCORES[4]},
                {'model_id': 5, 'model_name': 'SVR', 'metrics': CONCRETE_SCORES[5]}
            ]
        },
        'auto-price': {
            'dataset_name': 'Automobile Price Regression',
            'task_type': 'regression',
            'target': 'Vehicle Price (USD)',
            'models': [
                {'model_id': 1, 'model_name': 'LinearRegression', 'metrics': AUTO_PRICE_SCORES[1]},
                {'model_id': 2, 'model_name': 'Ridge', 'metrics': AUTO_PRICE_SCORES[2]},
                {'model_id': 3, 'model_name': 'KNeighborsRegressor', 'metrics': AUTO_PRICE_SCORES[3]},
                {'model_id': 4, 'model_name': 'DecisionTreeRegressor', 'metrics': AUTO_PRICE_SCORES[4]},
                {'model_id': 5, 'model_name': 'SVR', 'metrics': AUTO_PRICE_SCORES[5]}
            ]
        }
    }
    if dataset_filter and dataset_filter in datasets_meta:
        return datasets_meta[dataset_filter]
    return datasets_meta


def Heart_predictor(request, data: pd.DataFrame, model_code: int):
    Heart_models_file_paths = {
        1: MODELS_DIR / 'ML_Models' / 'Heart' / 'Logistic_model.pkl',
        2: MODELS_DIR / 'ML_Models' / 'Heart' / 'kNN_model.pkl',
        3: MODELS_DIR / 'ML_Models' / 'Heart' / 'tree_model.pkl',
        4: MODELS_DIR / 'ML_Models' / 'Heart' / 'svc_model.pkl'
    }

    scaler_path = MODELS_DIR / 'Scalers' / 'heart_scaler.pkl'
    model_path = Heart_models_file_paths.get(model_code)
    if not model_path:
        raise ValueError(f"Invalid model code: {model_code}")

    try:
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

            scaled_data = scaler.transform(data)
            pred = model.predict(scaled_data)

            response = {
                'Prediction': int(pred[0]),
                'model-accuracy': HEART_MODEL_SCORES.get(model_code)
            }
            return response
    except Exception as e:
        print(f"Heart predictor error: {e}")
        raise RuntimeError(f"Failed to load model/scaler or perform prediction: {e}") from e


def Diabetes_predictor(request, data: pd.DataFrame, model_code: int):
    Diabetes_models_file_paths = {
        1: MODELS_DIR / 'ML_Models' / 'Diabetes' / 'Logistic_model.pkl',
        2: MODELS_DIR / 'ML_Models' / 'Diabetes' / 'kNN_model.pkl',
        3: MODELS_DIR / 'ML_Models' / 'Diabetes' / 'tree_model.pkl',
        4: MODELS_DIR / 'ML_Models' / 'Diabetes' / 'svc_model.pkl'
    }

    scaler_path = MODELS_DIR / 'Scalers' / 'diabetes_scaler.pkl'
    model_path = Diabetes_models_file_paths.get(model_code)
    if not model_path:
        raise ValueError(f"Invalid model code: {model_code}")

    try:
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

            scaled_data = scaler.transform(data)
            pred = model.predict(scaled_data)

            response = {
                'Prediction': int(pred[0]),
                'model-accuracy': DIABETES_MODEL_SCORES.get(model_code)
            }
            return response
    except Exception as e:
        print(f"Diabetes predictor error: {e}")
        raise RuntimeError(f"Failed to load model/scaler or perform prediction: {e}") from e



def California_Housing_predictor(request, data:pd.DataFrame, model_code:int):
    California_Model_Paths = {
        1: MODELS_DIR / 'ML_Models' / 'California_Housing' / 'linear_model.pkl',
        2: MODELS_DIR / 'ML_Models' / 'California_Housing' / 'ridge_model.pkl',
        3: MODELS_DIR / 'ML_Models' / 'California_Housing' / 'kNN_model.pkl',
        4: MODELS_DIR / 'ML_Models' / 'California_Housing' / 'tree_model.pkl',
        5: MODELS_DIR / 'ML_Models' / 'California_Housing' / 'svr_model.pkl',
    }

    scaler_path = MODELS_DIR / 'Scalers' / 'california_housing.pkl'

    model_path = California_Model_Paths.get(model_code)
    if not model_path:
        raise ValueError(f"Invalid model code: {model_code}")

    try: 
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
            scaled_data = scaler.transform(data)
            pred = model.predict(scaled_data)

            response = {
                'Prediction': float(pred[0]),
                'model-accuracy': CALIFORNIA_HOUSING_SCORES.get(model_code)
            }
            return response
    except Exception as e:
        print(f"California Housing predictor error: {e}")
        raise RuntimeError(f"Failed to load model/scaler or perform prediction: {e}") from e


def Concrete_predictor(request, data:pd.DataFrame, model_code:int):
    Concrete_Model_Paths = {
        1: MODELS_DIR / 'ML_Models' / 'Concrete' / 'linear_model.pkl',
        2: MODELS_DIR / 'ML_Models' / 'Concrete' / 'ridge_model.pkl',
        3: MODELS_DIR / 'ML_Models' / 'Concrete' / 'kNN_model.pkl',
        4: MODELS_DIR / 'ML_Models' / 'Concrete' / 'tree_model.pkl',
        5: MODELS_DIR / 'ML_Models' / 'Concrete' / 'svr_model.pkl',
    }

    scaler_path = MODELS_DIR / 'Scalers' / 'concrete_scaler.pkl'

    model_path = Concrete_Model_Paths.get(model_code)
    if not model_path:
        raise ValueError(f'Invalid model code: {model_code}')
    
    try:
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

            scaler_data = scaler.transform(data)
            pred = model.predict(scaler_data)

            response = {
                'Prediction': float(pred[0]),
                'model-accuracy': CONCRETE_SCORES.get(model_code)
            }

            return response
    except Exception as e:
        print(f'Concrete predictor error: {e}')
        raise RuntimeError(f'Failed to load model/scaler or perform prediction: {e}') from e




def Auto_Price_Predictor(request, data:pd.DataFrame, model_code:int):
    Auto_Model_Paths = {
        1: MODELS_DIR / 'ML_Models' / 'Auto Price' / 'linear_model.pkl',
        2: MODELS_DIR / 'ML_Models' / 'Auto Price' / 'ridge_model.pkl',
        3: MODELS_DIR / 'ML_Models' / 'Auto Price' / 'kNN_model.pkl',
        4: MODELS_DIR / 'ML_Models' / 'Auto Price' / 'tree_model.pkl',
        5: MODELS_DIR / 'ML_Models' / 'Auto Price' / 'svr_model.pkl'
    }

    scaler_path = MODELS_DIR / "Scalers" / "auto_scaler.pkl"

    model_path = Auto_Model_Paths.get(model_code)
    if not model_path:
        raise ValueError(f"Invalid model code: {model_code}")

    try:
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

            scaler_data = scaler.transform(data)
            pred = model.predict(scaler_data)

            response = {
                'Prediction': float(pred[0]),
                'model-accuracy': AUTO_PRICE_SCORES.get(model_code)
            }

            return response
    except Exception as e:
        print(f'Auto Predictor Error: {e}')
        raise RuntimeError(f'Failed to load model/scaler or perform prediction: {e}') from e
