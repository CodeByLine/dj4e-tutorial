from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('autos', autos.as_view, name='autos'),
    # path('autolist/', views.auto_list, name='auto_list'),
    # path('auto/<int:id>/', views.post_detail, name='auto_detail'),
    # path('auto/<int:id>/update', views.post_detail, name='auto_update'),
    # path('auto/create/', views.post_create, name='auto_create'),

]