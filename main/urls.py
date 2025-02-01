from django.urls import path
from . import views

app_name = 'AgriPro'

urlpatterns = [
    path('',views.index, name='index'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('steps',views.step,name="step"),
]

