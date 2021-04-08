from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'hello'

# Note use of plural for list view and singular for detail view
urlpatterns = [
     path('', views.hello, name='hello'),
 
    # path('', TemplateView.as_view(template_name='hello/hello.html')),
    ]