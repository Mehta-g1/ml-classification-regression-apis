from django.shortcuts import render
from .predictor import HEART_PREDICTOR_MODEL_CODE, Heart_predictor, Diabetes_predictor
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json

@csrf_exempt
def Heart(request):
    if request.method == "POST":
        model_name = request.POST.get('model-name')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        cp = request.POST.get('cp')
        trestbps = request.POST.get('trestbps')
        chol = request.POST.get('chol')
        fbs = request.POST.get('fbs')
        restecg = request.POST.get('restecg')
        thalach = request.POST.get('thalach')
        exang = request.POST.get('exang')
        oldpeak = request.POST.get('oldpeak')
        slope = request.POST.get('slope')
        ca = request.POST.get('ca')
        thal = request.POST.get('thal')


        data = {
            'age' : age,
            'sex': sex,
            'cp':cp,
            'trestbps':trestbps,
            'chol':chol,
            'fbs':fbs,
            'restecg':restecg,
            'thalach': thalach,
            'exang':exang,
            'oldpeak':oldpeak,
            'slope':slope,
            'ca':ca,
            'thal':thal
        }

        df = pd.DataFrame([data])
        df = df.apply(pd.to_numeric)
        model_code = HEART_PREDICTOR_MODEL_CODE.get(model_name)
        if not model_code:
            return JsonResponse({
                'status': 'Bad Request',
                'message': 'Wrong Model Name',
                'model-name':model_name,
                'output': {
                    "model_id": HEART_PREDICTOR_MODEL_CODE.get(model_name),
                    "prediction": 'null'
                }
            }, status = 400)
        response = Heart_predictor(
            request=request,
            model_code=HEART_PREDICTOR_MODEL_CODE.get(model_name),
            data = df
        )
        
        response['Prediction'] = int(response['Prediction'])

        # print('='*60, '\n')
        # print(data)
        # print(response)
        # print(HEART_PREDICTOR_MODEL_CODE.get(model_name))
        # print('\n','='*60, '\n')

        return JsonResponse({
                'status': 'Ok',
                'message': 'Success',
                'model-name':model_name,
                'output': response
            }, status = 200)
    return HttpResponse('you are at right place')

@csrf_exempt
def Diabetes(request):
    if request.method == "POST":
        model_name = request.POST.get('model-name')
        age = request.POST.get('age')
        bmi = request.POST.get('bmi')
        family_history_diabetes = request.POST.get('family_history_diabetes')
        hypertension_history = request.POST.get('hypertension_history')
        glucose_fasting = request.POST.get('glucose_fasting')
        hba1c = request.POST.get('hba1c')
        physical_activity_minutes_per_week = request.POST.get('physical_activity_minutes_per_week')
        cardiovascular_history =request.POST.get('cardiovascular_history')
        gender = request.POST.get('gender')
        smoking_status = request.POST.get('smoking_status')
        

        data = {
            'age':age,
            'bmi':bmi,
            'family_history_diabetes': 1 if family_history_diabetes=='1' else 0,
            'hypertension_history': 1 if hypertension_history=='1' else 0,
            'glucose_fasting': glucose_fasting,
            'hba1c' : hba1c,
            'physical_activity_minutes_per_week': physical_activity_minutes_per_week,
            'cardiovascular_history':cardiovascular_history,
        }

        # gender cleaning
        gender_clean = str(gender).strip().lower()
        data['gender_Male'] = 1 if gender_clean == 'male' else 0
        data['gender_Other'] = 1 if gender_clean == 'other' else 0

        # smoking fix
        smoking_status_clean = str(smoking_status).strip().lower()
        data['smoking_status_Former'] = 1 if smoking_status_clean == "former" else 0
        data['smoking_status_Never'] = 1 if smoking_status_clean == 'never' else 0

        print('\n','='*60,'\n')

        print(data)

        df = pd.DataFrame([data])
        df = df.apply(pd.to_numeric)

        
        response = Diabetes_predictor(request, df, HEART_PREDICTOR_MODEL_CODE.get(model_name))

        response['Prediction'] = int(response['Prediction'])

        print('\n','='*60,'\n')

        print(data)
        print()
        print(df)
        print()
        print(response)
        print('\n','='*60,'\n')

        return JsonResponse({
                'status': 'Ok',
                'message': 'Success',
                'model-name':model_name,
                'output': response
            }, status = 200)
    return HttpResponse('you are at right place {Diabetes}')

