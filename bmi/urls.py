from django.urls import path
from . import views

urlpatterns = [
    path('', views.bmi_view, name='bmi'),
]
