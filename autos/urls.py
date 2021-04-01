from django.urls import path
from . import views 

urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('autos/', views.Autos.as_view(), name='autos'),
    path('autolist/', views.AutoList.as_view(), name='auto_list'),
    path('autocreate/', views.AutoCreate.as_view(), name='auto_create'),
    # path('create/', views.AutoCreate.as_view(), name='auto_create'),
    path('auto/<int:id>/', views.AutoDetail.as_view, name='auto_detail'),
    # path('auto/<int:id>/update', views.auto_detail, name='auto_update'),
    
]