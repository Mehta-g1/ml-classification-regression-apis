from django.urls import path
from .views import Heart, Diabetes, California_Housing, Concrete, Auto



urlpatterns = [
    path('heart/', Heart, name='heart'),
    path('diabetes/', Diabetes, name='diabetes'),
    path('california-housing/', California_Housing, name='california'),
    path('concrete/', Concrete, name='concrete'),
    path('auto-price/', Auto, name='auto')

]