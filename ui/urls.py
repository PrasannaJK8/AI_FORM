from django.urls import path
from . import views

urlpatterns = [
    path('voice_form_english/', views.voice_form_english.as_view(), name='voice_form_english'),
]