from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Image_Classifier import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name='results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
