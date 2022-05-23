from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('ENDTURN',views.ENDTURN),
]