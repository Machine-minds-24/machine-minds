# dreamapp_project/urls.py
from django.contrib import admin
from django.urls import path
from dreamapp.views import dream_app_input

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dream_app_input, name='dream_app_input'),
]
