from django.urls import path
from . import views

urlpatterns = [
	path('', views.list, name='list'),
	path('/1.csv', views.process_file, name='process_file')
]