from django.urls import path
from .views import Heart, Diabetes



urlpatterns = [
    path('heart/', Heart, name='heart'),
    path('diabetes/', Diabetes, name='diabetes')

]