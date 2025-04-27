from django.urls import path
from . import views

urlpatterns = [
    # Registro y login
    path("register/", views.registerView, name='register_view'),
    path('verify/<uuid:token>/', views.verifyEmail, name='verify_email'),
    path('login/', views.loginView, name='login_view'),
    path("logout/',", views.logoutView, name='llogout_view'),
    path("update/", views.updateUser, name='update_user_view'),
    path("delete/", views.deleteUser, name='delete_user_view'),
]