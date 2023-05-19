# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Internal:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from .import views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app_name = 'account'

# Urls for all the pages in the account app
urlpatterns = [
    path('', views.profile_page, name='profile'),
    path('update-profile/', views.profile_update, name='update-profile'),
    path('register', views.register, name='register'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout_page, name='logout'),
    path(
        'validate-username',
        csrf_exempt(views.Usernamevalidation.as_view()),
        name='validate-username'
        ),
    path(
        'validate-email',
        csrf_exempt(views.validate_email), name='validate-email'),
    path('confirmation', views.confirm_page, name='confirmation'),
]
