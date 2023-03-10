from django.urls import path
from .import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.restaurant, name='home'),
    path('<int:id>/<str:slug>/', views.table_detail, name='table-detail'),
    path('reservations', views.reservation_list, name='reservations'),
    path('reservation/<int:id>/', views.reservation_edit, name='reservation-edit'),
    path('reservation/delete/<int:id>/', views.reservation_delete, name='reservation-delete'),
]
