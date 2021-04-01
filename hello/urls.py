from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'hello'

# Note use of plural for list view and singular for detail view
urlpatterns = [
    path('', views.myview),
    ]