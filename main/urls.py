from django.urls import path
from . import views

#app_name = 'AgriPro'

urlpatterns = [
    path('',views.index, name='index'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('steps',views.step,name="step"),
    path('register/' ,views.register_view , name='register'),
    path('login/' ,views.login_view , name='login'),
    path('logout/' ,views.logout_view , name='logout'),
    path('recommend/' ,views.recommend_crop, name='recommend_crop'),
]

