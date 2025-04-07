from django.urls import path
from . import views

urlpatterns = [
    # Registro y login
    path("register/", views.registerView, name='register_view'),
    path('login/', views.loginView, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path("updateUser/<int:user_id>/',", views.updateUser, name='update_user'),
]