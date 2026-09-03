"""
Dynamic Dataset Samples Extractor
Reads authentic test samples directly from the raw dataset CSV and Excel files.
Provides at least 10 real sample rows per dataset with their ground-truth values.
"""

from pathlib import Path
import pandas as pd
import math

BASE_DATASET_DIR = Path(__file__).resolve().parent.parent / 'Datasets'

def _load_heart_samples():
    try:
        csv_path = BASE_DATASET_DIR / 'Classification datasets' / 'Heart Disease' / 'heart.csv'
        df = pd.read_csv(csv_path)
        features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        df_unique = df.drop_duplicates(subset=features)
        
        samples = []
        for i, (_, row) in enumerate(df_unique.head(12).iterrows()):
            target = int(row['target'])
            samples.append({
                'id': f'heart-sample-{i+1}',
                'row_index': i + 1,
                'title': f'Patient #{i+1} ({int(row["age"])}yo {"Male" if row["sex"] == 1 else "Female"})',
                'description': f'Chest pain type {int(row["cp"])}, Resting BP: {int(row["trestbps"])} mmHg, Chol: {int(row["chol"])} mg/dL, Max HR: {int(row["thalach"])} bpm.',
                'actual_target': target,
                'ground_truth': 'Heart Disease Risk (Class 1)' if target == 1 else 'Normal / No Risk (Class 0)',
                'data': {feat: float(row[feat]) for feat in features}
            })
        return samples
    except Exception as e:
        print(f"Error reading heart.csv: {e}")
        return []

def _load_diabetes_samples():
    try:
        csv_path = BASE_DATASET_DIR / 'Classification datasets' / 'Diabetes' / 'diabetes_dataset.csv'
        df = pd.read_csv(csv_path)
        features = ['age', 'bmi', 'glucose_fasting', 'hba1c', 'physical_activity_minutes_per_week', 'cardiovascular_history', 'family_history_diabetes', 'hypertension_history', 'gender', 'smoking_status']
        
        samples = []
        for i, (_, row) in enumerate(df.head(12).iterrows()):
            target = int(row['diagnosed_diabetes'])
            samples.append({
                'id': f'diabetes-sample-{i+1}',
                'row_index': i + 1,
                'title': f'Subject #{i+1} ({int(row["age"])}yo {row["gender"]})',
                'description': f'BMI: {round(float(row["bmi"]), 1)}, Fasting Glucose: {round(float(row["glucose_fasting"]), 1)} mg/dL, HbA1c: {round(float(row["hba1c"]), 2)}%, Activity: {round(float(row["physical_activity_minutes_per_week"]))} min/wk.',
                'actual_target': target,
                'ground_truth': 'Diabetic / High Risk (Class 1)' if target == 1 else 'Non-Diabetic (Class 0)',
                'data': {
                    'age': float(row['age']),
                    'bmi': round(float(row['bmi']), 1),
                    'glucose_fasting': round(float(row['glucose_fasting']), 1),
                    'hba1c': round(float(row['hba1c']), 2),
                    'physical_activity_minutes_per_week': round(float(row['physical_activity_minutes_per_week']), 1),
                    'cardiovascular_history': float(row['cardiovascular_history']),
                    'family_history_diabetes': str(int(row['family_history_diabetes'])),
                    'hypertension_history': str(int(row['hypertension_history'])),
                    'gender': str(row['gender']),
                    'smoking_status': str(row['smoking_status'])
                }
            })
        return samples
    except Exception as e:
        print(f"Error reading diabetes_dataset.csv: {e}")
        return []

def _load_california_samples():
    try:
        csv_path = BASE_DATASET_DIR / 'Regression datasets' / 'California Housing' / 'california_housing.csv'
        df = pd.read_csv(csv_path)
        features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
        
        samples = []
        for i, (_, row) in enumerate(df.head(12).iterrows()):
            val = round(float(row['MedHouseVal']), 3)
            dollars = int(round(val * 100000))
            samples.append({
                'id': f'california-sample-{i+1}',
                'row_index': i + 1,
                'title': f'California Block #{i+1}',
                'description': f'Median Income: ${round(float(row["MedInc"]) * 10, 1)}k, House Age: {int(row["HouseAge"])} yrs, {round(float(row["AveRooms"]), 1)} avg rooms.',
                'actual_target': val,
                'ground_truth': f'${dollars:,} USD ({val} in $100k units)',
                'data': {feat: round(float(row[feat]), 4) for feat in features}
            })
        return samples
    except Exception as e:
        print(f"Error reading california_housing.csv: {e}")
        return []

def _load_concrete_samples():
    try:
        excel_path = BASE_DATASET_DIR / 'Regression datasets' / 'Concrete Data' / 'Concrete_Data.xls'
        df = pd.read_excel(excel_path)
        con_col_map = {
            'Cement (component 1)(kg in a m^3 mixture)': 'cement',
            'Blast Furnace Slag (component 2)(kg in a m^3 mixture)': 'slag',
            'Fly Ash (component 3)(kg in a m^3 mixture)': 'fly_ash',
            'Water  (component 4)(kg in a m^3 mixture)': 'water',
            'Superplasticizer (component 5)(kg in a m^3 mixture)': 'superplasticizer',
            'Coarse Aggregate  (component 6)(kg in a m^3 mixture)': 'coarse_aggregate',
            'Fine Aggregate (component 7)(kg in a m^3 mixture)': 'fine_aggregate',
            'Age (day)': 'age'
        }
        target_col = 'Concrete compressive strength(MPa, megapascals) '
        
        samples = []
        for i, (_, row) in enumerate(df.head(12).iterrows()):
            strength = round(float(row[target_col]), 2)
            samples.append({
                'id': f'concrete-sample-{i+1}',
                'row_index': i + 1,
                'title': f'Concrete Mixture Batch #{i+1}',
                'description': f'Cement: {round(float(row["Cement (component 1)(kg in a m^3 mixture)"]), 1)} kg/m³, Water: {round(float(row["Water  (component 4)(kg in a m^3 mixture)"]), 1)} kg/m³, Curing Age: {int(row["Age (day)"])} days.',
                'actual_target': strength,
                'ground_truth': f'{strength} MPa Compressive Strength',
                'data': {new_k: round(float(row[orig_k]), 2) for orig_k, new_k in con_col_map.items()}
            })
        return samples
    except Exception as e:
        print(f"Error reading Concrete_Data.xls: {e}")
        return []

def _load_auto_samples():
    try:
        csv_path = BASE_DATASET_DIR / 'Regression datasets' / 'Automobile' / 'auto_price.csv'
        df = pd.read_csv(csv_path)
        features = ['horsepower', 'curb-weight', 'engine-size', 'highway-mpg', 'city-mpg', 'wheel-base', 'length', 'width']
        df_clean = df.dropna(subset=features + ['price'])
        
        samples = []
        for i, (_, row) in enumerate(df_clean.head(12).iterrows()):
            price = int(round(float(row['price'])))
            make = str(row.get('make', 'Vehicle')).title()
            body = str(row.get('body-style', '')).title()
            samples.append({
                'id': f'auto-sample-{i+1}',
                'row_index': i + 1,
                'title': f'{make} {body} #{i+1}',
                'description': f'{round(float(row["horsepower"]))} HP, {round(float(row["curb-weight"]))} lbs, {round(float(row["engine-size"]))} ci engine, {round(float(row["highway-mpg"]))} HWY MPG.',
                'actual_target': price,
                'ground_truth': f'${price:,} USD',
                'data': {feat: round(float(row[feat]), 1) for feat in features}
            })
        return samples
    except Exception as e:
        print(f"Error reading auto_price.csv: {e}")
        return []

# Cache extracted samples
_CACHED_SAMPLES = None

def get_dataset_samples(dataset_filter: str = None):
    """
    Returns authentic test samples extracted from original dataset CSV/Excel files.
    """
    global _CACHED_SAMPLES
    if _CACHED_SAMPLES is None:
        _CACHED_SAMPLES = {
            'heart': {
                'dataset_id': 'heart',
                'name': 'Heart Disease Risk',
                'samples': _load_heart_samples()
            },
            'diabetes': {
                'dataset_id': 'diabetes',
                'name': 'Diabetes Risk Prediction',
                'samples': _load_diabetes_samples()
            },
            'california-housing': {
                'dataset_id': 'california-housing',
                'name': 'California Housing Prices',
                'samples': _load_california_samples()
            },
            'concrete': {
                'dataset_id': 'concrete',
                'name': 'Concrete Compressive Strength',
                'samples': _load_concrete_samples()
            },
            'auto-price': {
                'dataset_id': 'auto-price',
                'name': 'Automobile Price Prediction',
                'samples': _load_auto_samples()
            }
        }
    
    if dataset_filter and dataset_filter in _CACHED_SAMPLES:
        return _CACHED_SAMPLES[dataset_filter]
    return _CACHED_SAMPLES
