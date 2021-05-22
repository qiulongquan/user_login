from django.urls import path
from . import views

app_name = 'show_predict_data'

urlpatterns = [
    path('index/', views.index, name='index'),
]
