import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from pathlib import Path
import numpy as np
import pandas as pd


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

AUTO_SCORES = {
    1: {'r2_score': 0.7992, 'mean_absolute_error': 2815.49, 'mean_squared_error': 15659145.60},
    2: {'r2_score': 0.7754, 'mean_absolute_error': 2994.33, 'mean_squared_error': 17509085.31},
    3: {'r2_score': 0.7594, 'mean_absolute_error': 2319.07, 'mean_squared_error': 18760831.27},
    4: {'r2_score': 0.9246, 'mean_absolute_error': 1712.85, 'mean_squared_error': 5877138.08},
    5: {'r2_score': 0.7589, 'mean_absolute_error': 2984.95, 'mean_squared_error': 18801163.42}
}

def get_all_dataset_accuracies(dataset_filter: str = None):
    """Returns structured accuracy metrics for models across datasets."""
    datasets_meta = {
        'heart': {
            'dataset_id': 'heart',
            'name': 'Heart Disease Risk',
            'type': 'classification',
            'target': 'Heart Disease Risk (1: Risk Present, 0: Normal)',
            'models': [
                {
                    'model_name': CLASSIFIER_CODE_TO_NAME[code],
                    'model_code': code,
                    'metrics': HEART_MODEL_SCORES[code]
                }
                for code in sorted(HEART_MODEL_SCORES.keys())
            ]
        },
        'diabetes': {
            'dataset_id': 'diabetes',
            'name': 'Diabetes Risk Prediction',
            'type': 'classification',
            'target': 'Diabetes Risk (1: Positive, 0: Negative)',
            'models': [
                {
                    'model_name': CLASSIFIER_CODE_TO_NAME[code],
                    'model_code': code,
                    'metrics': DIABETES_MODEL_SCORES[code]
                }
                for code in sorted(DIABETES_MODEL_SCORES.keys())
            ]
        },
        'california-housing': {
            'dataset_id': 'california-housing',
            'name': 'California Housing Prices',
            'type': 'regression',
            'target': 'Median House Value ($100k units)',
            'models': [
                {
                    'model_name': REGRESSOR_CODE_TO_NAME[code],
                    'model_code': code,
                    'metrics': CALIFORNIA_HOUSING_SCORES[code]
                }
                for code in sorted(CALIFORNIA_HOUSING_SCORES.keys())
            ]
        },
        'concrete': {
            'dataset_id': 'concrete',
            'name': 'Concrete Compressive Strength',
            'type': 'regression',
            'target': 'Compressive Strength (MPa)',
            'models': [
                {
                    'model_name': REGRESSOR_CODE_TO_NAME[code],
                    'model_code': code,
                    'metrics': CONCRETE_SCORES[code]
                }
                for code in sorted(CONCRETE_SCORES.keys())
            ]
        },
        'auto-price': {
            'dataset_id': 'auto-price',
            'name': 'Automobile Price Prediction',
            'type': 'regression',
            'target': 'Vehicle Price (USD)',
            'models': [
                {
                    'model_name': REGRESSOR_CODE_TO_NAME[code],
                    'model_code': code,
                    'metrics': AUTO_SCORES[code]
                }
                for code in sorted(AUTO_SCORES.keys())
            ]
        }
    }
    if dataset_filter and dataset_filter in datasets_meta:
        return datasets_meta[dataset_filter]
    return datasets_meta


def Heart_predictor(request, data: pd.DataFrame, model_code: int):
    Heart_models_file_paths = {
        1: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Heart' / 'Logistic_model.pkl',
        2: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Heart' / 'kNN_model.pkl',
        3: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Heart' / 'tree_model.pkl',
        4: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Heart' / 'svc_model.pkl'
    }

    scaler_path = Path.cwd() / 'ML_models and scalers' / 'Scalers' / 'heart_scaler.pkl'
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
        1: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Diabetes' / 'Logistic_model.pkl',
        2: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Diabetes' / 'kNN_model.pkl',
        3: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Diabetes' / 'tree_model.pkl',
        4: Path.cwd() / 'ML_models and scalers' / 'ML_Models' / 'Diabetes' / 'svc_model.pkl'
    }

    scaler_path = Path.cwd() / 'ML_models and scalers' / 'Scalers' / 'diabetes_scaler.pkl'
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
    California_Housing_Scores = {
        1: {
            'r2_score' : 0.6009790143129108,
            'mean_absolute_error' : 0.5366527228153435,
            'mean_squared_error' : 0.5444842122132871,
        },
        5: {
            'r2_score' : 0.7416209399588087,
            'mean_absolute_error' : 0.39244257311378744,
            'mean_squared_error' : 0.3525712280939052,
        },
        3: {
            'r2_score' : 0.7413908302899435,
            'mean_absolute_error' : 0.3961278082197597,
            'mean_squared_error' : 0.35288522431532965,
        },
        4: {
            'r2_score' : 0.7277476106082925,
            'mean_absolute_error' : 0.4010641743973573,
            'mean_squared_error' : 0.37150208404671714,
        },
        2: {
            'r2_score' : 0.5972392061655951,
            'mean_absolute_error' : 0.5387135886810602,
            'mean_squared_error' : 0.5495873686034546,
        }
    }

    California_Model_Paths = {
        1: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'California_Housing'/ 'linear_model.pkl',
        2: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'California_Housing'/ 'ridge_model.pkl',
        3: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'California_Housing'/ 'kNN_model.pkl',
        4: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'California_Housing'/ 'tree_model.pkl',
        5: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'California_Housing'/ 'svr_model.pkl',
    }

    scaler_path = Path.cwd()/'Ml_models and scalers'/'Scalers'/'california_housing.pkl'

    model = ''
    scaler = ''

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
                'Prediction': pred[0],
                'model-accuracy': California_Housing_Scores.get(model_code)
            }
            return response
    except Exception as e:
        print(f"California Housing predictor error: {e}")
        raise RuntimeError(f"Failed to load model/scaler or perform prediction: {e}") from e


def Concrete_predictor(request, data:pd.DataFrame, model_code:int):
    Concrete_Scores = {
        1 : {
            'r2_score' : 0.6128899126006704,
            'mean_absolute_error' : 8.186575235450505,
            'mean_squared_error' : 104.92832620839133,
        },
        2 : {
            'r2_score' : 0.6133465755293246,
            'mean_absolute_error' : 8.186766318650339,
            'mean_squared_error' : 104.80454520059837,
        },
        3 : {
            'r2_score' : 0.8030112619681574,
            'mean_absolute_error' : 5.492273492952563,
            'mean_squared_error' : 53.39488490844302,
        },
        4 : {
            'r2_score' : 0.8797892499240952,
            'mean_absolute_error' : 3.7900905486098186,
            'mean_squared_error' : 32.583787424553115,
        },
        5 : {
            'r2_score' : 0.8867083187224074,
            'mean_absolute_error' : 3.9354438747834637,
            'mean_squared_error' : 30.7083356304523,
        }
    }

    Concrete_Model_Paths = {
        1: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Concrete'/ 'linear_model.pkl',
        2: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Concrete'/ 'ridge_model.pkl',
        3: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Concrete'/ 'kNN_model.pkl',
        4: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Concrete'/ 'tree_model.pkl',
        5: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Concrete'/ 'svr_model.pkl',
    }

    scaler_path = Path.cwd()/'Ml_models and scalers'/'Scalers'/'concrete_scaler.pkl'

    model = ''
    scaler = ''

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
                'Prediction' : pred[0],
                'model-accuracy' : Concrete_Scores.get(model_code)
            }

            return response
    except Exception as e:
        print(f'Concrete predictor error: {e}')
        raise RuntimeError(f'Failed to load model/scaler or perform prediction: {e}') from e




def Auto_Price_Predictor(request, data:pd.DataFrame, model_code:int):
    Auto_Scores = {
    1 : {
        'r2_score' : 0.7991698250994186,
        'mean_absolute_error' : 2815.4906790660093,
        'mean_squared_error' : 15659145.596779807
    },
    2 : {
        'r2_score' : 0.7754441553546209,
        'mean_absolute_error' : 2994.3329040058993,
        'mean_squared_error' : 17509085.31375123
    },
    3 : {
        'r2_score' : 0.7593903829798968,
        'mean_absolute_error' : 2319.0700251326366,
        'mean_squared_error' : 18760831.268350992
    },
    4 : {
        'r2_score' : 0.9246250913272545,
        'mean_absolute_error' : 1712.8520810581238,
        'mean_squared_error' : 5877138.083631109
    },
    5 : {
        'r2_score' : 0.7588731189264806,
        'mean_absolute_error' : 2984.947642911973,
        'mean_squared_error' : 18801163.420272052
    }
}

    Auto_Model_Paths = {
        1: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Auto Price'/ 'linear_model.pkl',
        2: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Auto Price'/ 'ridge_model.pkl',
        3: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Auto Price'/ 'kNN_model.pkl',
        4: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Auto Price'/ 'tree_model.pkl',
        5: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Auto Price'/ 'svr_model.pkl'
    }

    scaler_path = Path.cwd()/ "Ml_models and scalers" / "Scalers" / "auto_scaler.pkl"

    model = ''
    scaler = ''

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
                'Prediction' : pred[0],
                'model-accuracy' : Auto_Scores.get(model_code)
            }

            return response
    except Exception as e:
        print(f'Auto Predictor Error: {e}')
        raise RuntimeError(f'Failed to load model/scaler or perform prediction: {e}') from e

