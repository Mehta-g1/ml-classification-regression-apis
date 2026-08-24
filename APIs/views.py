from django.shortcuts import render
from .predictor import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import pandas as pd
import json

def get_request_data(request):

    if request.content_type == 'application/json':
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return None
    return {k: v for k, v in request.POST.items()}


def validate_numeric_fields(data, fields):

    errors = []
    cleaned = {}
    for field in fields:
        val = data.get(field)

        if val is None or str(val).strip() == "":
            errors.append(f"Field '{field}' is required.")
        else:
            try:
                cleaned[field] = float(val)
            except ValueError:
                errors.append(f"Field '{field}' must be numeric (received: '{val}').")
    return cleaned, errors


@csrf_exempt
@require_http_methods(["POST"])
def Heart(request):

    data = get_request_data(request)
    if data is None:
        return JsonResponse({
            'status': 'Bad Request',
            'message': 'Invalid JSON format in request body.',
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)
    

    model_name_raw = data.get('model-name')
    if model_name_raw is None or str(model_name_raw).strip() == "":
        return JsonResponse({
            'status': 'Bad Request',
            'message': "Missing required field: 'model-name'.",
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)
        
    model_name = str(model_name_raw).strip()
    model_code = CLASSIFIER_PREDICTOR_MODEL_CODE.get(model_name)
    if not model_code:
        return JsonResponse({
            'status': 'Bad Request',
            'message': f"Wrong Model Name: '{model_name}'. Available options: {list(CLASSIFIER_PREDICTOR_MODEL_CODE.keys())}",
            'model-name': model_name,
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    # 3. Validate clinical features
    required_features = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    cleaned_features, errors = validate_numeric_fields(data, required_features)
    
    if errors:
        return JsonResponse({
            'status': 'Unprocessable Entity',
            'message': 'Input validation failed. Please check the errors field for details.',
            'errors': errors,
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=422)


    try:

        df = pd.DataFrame([cleaned_features])[required_features]
        
        response = Heart_predictor(
            request=request,
            model_code=model_code,
            data=df
        )
        
        if response is None or 'Prediction' not in response:
            raise ValueError("Predictor returned an empty or invalid prediction payload.")

        # Ensure prediction is converted to integer
        response['Prediction'] = int(response['Prediction'])

        return JsonResponse({
            'status': 'Ok',
            'message': 'Success',
            'model-name': model_name,
            'output': response
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'status': 'Internal Server Error',
            'message': f'Prediction engine failure: {str(e)}',
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def Diabetes(request):

    data = get_request_data(request)
    if data is None:
        return JsonResponse({
            'status': 'Bad Request',
            'message': 'Invalid JSON format in request body.',
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    model_name_raw = data.get('model-name')
    if model_name_raw is None or str(model_name_raw).strip() == "":
        return JsonResponse({
            'status': 'Bad Request',
            'message': "Missing required field: 'model-name'.",
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    model_name = str(model_name_raw).strip()
    model_code = CLASSIFIER_PREDICTOR_MODEL_CODE.get(model_name)
    if not model_code:
        return JsonResponse({
            'status': 'Bad Request',
            'message': f"Wrong Model Name: '{model_name}'. Available options: {list(CLASSIFIER_PREDICTOR_MODEL_CODE.keys())}",
            'model-name': model_name,
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)


    numeric_features = [
        'age', 'bmi', 'glucose_fasting', 'hba1c', 
        'physical_activity_minutes_per_week', 'cardiovascular_history'
    ]
    cleaned_features, errors = validate_numeric_fields(data, numeric_features)


    family_history_raw = data.get('family_history_diabetes')
    hypertension_raw = data.get('hypertension_history')
    
    if family_history_raw is None or str(family_history_raw).strip() == "":
        errors.append("Field 'family_history_diabetes' is required.")
    if hypertension_raw is None or str(hypertension_raw).strip() == "":
        errors.append("Field 'hypertension_history' is required.")

    gender_raw = data.get('gender')
    smoking_status_raw = data.get('smoking_status')

    if gender_raw is None or str(gender_raw).strip() == "":
        errors.append("Field 'gender' is required.")
    if smoking_status_raw is None or str(smoking_status_raw).strip() == "":
        errors.append("Field 'smoking_status' is required.")

    if errors:
        return JsonResponse({
            'status': 'Unprocessable Entity',
            'message': 'Input validation failed. Please check the errors field for details.',
            'errors': errors,
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=422)

    family_history_str = str(family_history_raw).strip()
    hypertension_str = str(hypertension_raw).strip()
    gender_clean = str(gender_raw).strip().lower()
    smoking_status_clean = str(smoking_status_raw).strip().lower()

    model_data = {
        'age': cleaned_features['age'],
        'bmi': cleaned_features['bmi'],
        'family_history_diabetes': 1 if family_history_str == '1' else 0,
        'hypertension_history': 1 if hypertension_str == '1' else 0,
        'glucose_fasting': cleaned_features['glucose_fasting'],
        'hba1c': cleaned_features['hba1c'],
        'physical_activity_minutes_per_week': cleaned_features['physical_activity_minutes_per_week'],
        'cardiovascular_history': cleaned_features['cardiovascular_history'],
        'gender_Male': 1 if gender_clean == 'male' else 0,
        'gender_Other': 1 if gender_clean == 'other' else 0,
        'smoking_status_Former': 1 if smoking_status_clean == 'former' else 0,
        'smoking_status_Never': 1 if smoking_status_clean == 'never' else 0
    }

    expected_order = [
        'age', 'bmi', 'family_history_diabetes', 'hypertension_history',
        'glucose_fasting', 'hba1c', 'physical_activity_minutes_per_week', 'cardiovascular_history',
        'gender_Male', 'gender_Other', 'smoking_status_Former', 'smoking_status_Never'
    ]


    try:
        df = pd.DataFrame([model_data])[expected_order]
        
        response = Diabetes_predictor(request, df, model_code)
        if response is None or 'Prediction' not in response:
            raise ValueError("Predictor returned an empty or invalid prediction payload.")

        response['Prediction'] = int(response['Prediction'])

        return JsonResponse({
            'status': 'Ok',
            'message': 'Success',
            'model-name': model_name,
            'output': response
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'status': 'Internal Server Error',
            'message': f'Prediction engine failure: {str(e)}',
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def California_Housing(request):

    data = get_request_data(request)
    if data is None:
        return JsonResponse({
            'status': 'Bad Request',
            'message': 'Invalid JSON format in request body.',
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)


    model_name_raw = data.get('model-name')
    if model_name_raw is None or str(model_name_raw).strip() == "":
        return JsonResponse({
            'status': 'Bad Request',
            'message': "Missing required field: 'model-name'.",
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    model_name = str(model_name_raw).strip()
    model_code = REGRESSOR_PREDICTOR_MODEL_CODE.get(model_name)
    if not model_code:
        return JsonResponse({
            'status': 'Bad Request',
            'message': f"Wrong Model Name: '{model_name}'. Available options: {list(REGRESSOR_PREDICTOR_MODEL_CODE.keys())}",
            'model-name': model_name,
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    required_features = [
        'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 
        'Population', 'AveOccup', 'Latitude', 'Longitude'
    ]
    cleaned_features, errors = validate_numeric_fields(data, required_features)

    if errors:
        return JsonResponse({
            'status': 'Unprocessable Entity',
            'message': 'Input validation failed. Please check the errors field for details.',
            'errors': errors,
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=422)


    try:
        df = pd.DataFrame([cleaned_features])[required_features]
        
        response = California_Housing_predictor(request, df, model_code)
        if response is None or 'Prediction' not in response:
            raise ValueError("Predictor returned an empty or invalid prediction payload.")

        response['Prediction'] = float(response['Prediction'])

        return JsonResponse({
            'status': 'Ok',
            'message': 'Success',
            'model-name': model_name,
            'output': response
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'status': 'Internal Server Error',
            'message': f'Prediction engine failure: {str(e)}',
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def Concrete(request):
    data = get_request_data(request)
    if data is None:
        return JsonResponse({
            'status': 'Bad Request',
            'message': 'Invalid JSON format in request body.',
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    model_name_raw = data.get('model-name')
    if model_name_raw is None or str(model_name_raw).strip() == "":
        return JsonResponse({
            'status': 'Bad Request',
            'message': "Missing required field: 'model-name'.",
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    model_name = str(model_name_raw).strip()
    model_code = REGRESSOR_PREDICTOR_MODEL_CODE.get(model_name)
    if not model_code:
        return JsonResponse({
            'status': 'Bad Request',
            'message': f"Wrong Model Name: '{model_name}'. Available options: {list(REGRESSOR_PREDICTOR_MODEL_CODE.keys())}",
            'model-name': model_name,
            'output': {
                'model_id': None,
                'prediction': 'null'
            }
        }, status=400)

    required_features = ['cement', 'slag', 'fly_ash', 'water', 'superplasticizer', 'coarse_aggregate', 'fine_aggregate', 'age']
    
    cleaned_features, errors = validate_numeric_fields(data, required_features)

    if errors:
        return JsonResponse({
            'status': 'Unprocessable Entity',
            'message': 'Input validation failed. Please check the errors field for details.',
            'errors': errors,
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=422)

    try:
        df = pd.DataFrame([cleaned_features])[required_features]
        response = Concrete_predictor(request, df, model_code)

        if response is None or 'Prediction' not in response:
            raise ValueError("Predictor returned an empty or invalid prediction payload")
        
        response['Prediction'] = float(response['Prediction'])

        return JsonResponse({
            'status': 'Ok',
            'message': 'Success',
            'model-name': model_name,
            'output': response
        }, status=200)

        
    except Exception as e:
        return JsonResponse({
            'status': 'Internal Server Error',
            'message': f'Prediction engine failure: {str(e)}',
            'model-name': model_name,
            'output': {
                'model_id': model_code,
                'prediction': 'null'
            }
        }, status=500)


