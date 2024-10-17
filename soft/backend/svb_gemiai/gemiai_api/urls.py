from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('process_prompt/', views.process_prompt, name='process_prompt'),
]
