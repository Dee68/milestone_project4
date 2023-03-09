from django.urls import path
from .import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.restaurant, name='home'),
    path('reservation', views.reserve_table, name='reservation'),
    path('<int:id>/<str:slug>/', views.table_detail, name='table-detail'),
]
