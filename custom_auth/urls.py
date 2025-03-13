from django.urls import path
from . import views

urlpatterns = [
    # Registro y login
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

     path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
]