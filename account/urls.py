from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views

app_name = 'account'

urlpatterns = [
    path('register', views.register, name='register'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout_page, name='logout'),
    # path('validate-username', csrf_exempt(views.validate_username), name='validate-username'),
    # path('validate-email', csrf_exempt(views.validate_email), name='validate-email'),
    # path('confirmation', views.confirm_page, name='confirmation'),
]
