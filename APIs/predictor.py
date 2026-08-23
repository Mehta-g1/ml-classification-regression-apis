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
    'LogisticRegression':1,
    'KNeighborsClassifier':2,
    'DecisionTreeClassifier':3,
    'SVC':4
}

REGRESSOR_PREDICTOR_MODEL_CODE = {
    'LinearRegression':1,
    'Ridge':2,
    'KNeighborsRegressor':3,
    'DecisionTreeRegressor':4,
    'SVR':5
}


def Heart_predictor(request, data: pd.DataFrame, model_code: int):

    Heart_models_file_paths = {
        1: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Heart'/ 'Logistic_model.pkl',
        2: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Heart'/ 'kNN_model.pkl',
        3: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Heart'/ 'tree_model.pkl',
        4: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Heart'/ 'svc_model.pkl'
    }

    Heart_Model_Scores = {
        1 : {
            'accuracy_score':0.7763157894736842,
            'recall_score': 0.8888888888888888,
            'f1_score': 0.7901234567901234,
        },
        2 : {
            'accuracy_score':0.7894736842105263,
            'recall_score': 0.9444444444444444,
            'f1_score': 0.8095238095238095,
        },
        3: {
            'accuracy_score':0.7763157894736842,
            'recall_score': 0.8888888888888888,
            'f1_score': 0.7901234567901234,
        },
        4 : {
            'accuracy_score' : 0.75,
            'recall_score': 0.8333333333333334,
            'f1_score': 0.759493670886076,
        }
    }

    scaler_path = Path.cwd()/'Ml_models and scalers'/'Scalers'/'heart_scaler.pkl'
    model = ''
    scaler = ''
    # Retrieve the model file path based on the model code mapping
    model_path = Heart_models_file_paths.get(model_code)
    if not model_path:
        raise ValueError(f"Invalid model code: {model_code}")

    try: 
        # 1. Load the fitted scaler object
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        # 2. Load the trained machine learning model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
            # 3. Transform input data using the loaded scaler and perform prediction
            scaled_data = scaler.transform(data)
            pred = model.predict(scaled_data)

            # 4. Return both the prediction and the performance scores of the selected model
            response = {
                'Prediction': pred[0],
                'model-accuracy': Heart_Model_Scores.get(model_code)
            }
            return response
    except Exception as e:
        # Print error details to terminal for developer tracking and re-raise
        print(f"Heart predictor error: {e}")
        raise RuntimeError(f"Failed to load model/scaler or perform prediction: {e}") from e



def Diabetes_predictor(request, data:pd.DataFrame, model_code:int):
    Diabetes_model_scores = {
        1 : {
            'sccuracy_score' : 0.8847,
            'f1_score' : 0.8946069469835466,
            'recall_score' : 0.8175591011611394,
        },
        2 : {
            'accuracy_score':0.87425,
            'recall_score': 0.8621669033497619,
            'f1_score': 0.8913935311137021,
        },
        3: {
            'sccuracy_score' : 0.9204,
            'f1_score' : 0.9287695749440716,
            'recall_score' : 0.867011945535043,
        },
        4 : {
            'accuracy_score':0.8996,
            'recall_score': 0.8714393116698689,
            'f1_score': 0.9122070654074851,
        }
    }

    Diabetes_models_file_paths = {
        1: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Diabetes'/ 'Logistic_model.pkl',
        2: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Diabetes'/ 'kNN_model.pkl',
        3: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Diabetes'/ 'tree_model.pkl',
        4: Path.cwd()/'Ml_models and scalers'/'ML_Models'/'Diabetes'/ 'svc_model.pkl'
    }

    scaler_path = Path.cwd()/'Ml_models and scalers'/'Scalers'/'diabetes_scaler.pkl'
    model = ''
    scaler = ''
    # Retrieve the model file path based on the model code mapping
    model_path = Diabetes_models_file_paths.get(model_code)
    if not model_path:
        raise ValueError(f"Invalid model code: {model_code}")

    try: 
        # 1. Load the fitted scaler object
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        # 2. Load the trained machine learning model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
            # 3. Transform input data using the loaded scaler and perform prediction
            scaled_data = scaler.transform(data)
            pred = model.predict(scaled_data)

            # 4. Return both the prediction and the performance scores of the selected model
            response = {
                'Prediction': pred[0],
                'model-accuracy': Diabetes_model_scores.get(model_code)
            }
            return response
    except Exception as e:
        # Print error details to terminal for developer tracking and re-raise
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
    # Retrieve the model file path based on the model code mapping
    model_path = California_Model_Paths.get(model_code)
    if not model_path:
        raise ValueError(f"Invalid model code: {model_code}")

    try: 
        # 1. Load the fitted scaler object
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        # 2. Load the trained machine learning model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
            # 3. Transform input data using the loaded scaler and perform prediction
            scaled_data = scaler.transform(data)
            pred = model.predict(scaled_data)

            # 4. Return both the prediction and the performance scores of the selected model
            response = {
                'Prediction': pred[0],
                'model-accuracy': California_Housing_Scores.get(model_code)
            }
            return response
    except Exception as e:
        # Print error details to terminal for developer tracking and re-raise
        print(f"California Housing predictor error: {e}")
        raise RuntimeError(f"Failed to load model/scaler or perform prediction: {e}") from e


