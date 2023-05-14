# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.urls import path
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Internal:
from .import views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


app_name = 'restaurant'

# Urls for all the pages in the restaurant app
urlpatterns = [
    path('', views.restaurant, name='home'),
    path('<int:id>/<str:slug>/', views.table_detail, name='table-detail'),
    path('reservations', views.reservation_list, name='reservations'),
    path(
        'reservation/edit/<int:id>/<str:customer>/',
        views.reservation_edit,
        name='reservation-edit'
        ),
    path(
        'reservation/delete/<int:id>/<str:customer>/',
        views.reservation_delete,
        name='reservation-delete'
        ),
    path('reviews/', views.review_list, name='reviews'),
    path('reviews/<str:slug>/', views.review_table, name='table-review'),
    path('reservation/login_user/', views.login_user, name='login-user'),
    path('foods', views.food_list, name='foods'),
    path('drinks', views.drink_list, name='drinks'),
]
