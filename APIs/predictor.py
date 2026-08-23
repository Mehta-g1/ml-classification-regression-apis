import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from pathlib import Path
from django.contrib import messages
import numpy as np
import pandas as pd


HEART_PREDICTOR_MODEL_CODE = {
    'LogisticRegression':1,
    'KNeighborsClassifier':2,
    'DecisionTreeClassifier':3,
    'SVC':4
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
    model_path = Heart_models_file_paths.get(model_code)

    try: 
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            pred = model.predict(scaler.transform(data))

            response = {
                'Prediction': pred[0],
                'model-accuracy': Heart_Model_Scores.get(model_code)
            }
            return response
    except Exception as e:
        messages.error(request, f"Error: {e}")
        print(f"error: {e}")

    return None



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
    model_path = Diabetes_models_file_paths.get(model_code)

    try: 
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            pred = model.predict(scaler.transform(data))

            response = {
                'Prediction': pred[0],
                'model-accuracy': Diabetes_model_scores.get(model_code)
            }
            return response
    except Exception as e:
        messages.error(request, f"Error: {e}")
        print(f"error: {e}")
        

    return None







