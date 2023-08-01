from .import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name = 'activate'),
    path('unuttumPassword/', views.unuttumPassword, name = 'unuttumPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name ='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name = 'resetPassword'),

    path('my_siparis/', views.my_siparis, name='my_siparis'),
    path('edit_profile/', views.edit_profile, name ='edit_profile'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('siparis_detail/<int:order_id>/', views.siparis_detail, name = 'siparis_detail' ),
]
