from django.urls import path

from worker import views

urlpatterns = [
    path('', views.index, name='index'),
]
