from django.urls import path

from . import views
app_name = 'rooms'
urlpatterns = [
    path('index/',views.index, name='index'),
]
