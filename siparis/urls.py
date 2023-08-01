from django.urls import path
from .import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('odemeler/', views.odemeler, name = 'odemeler'),
    path('siparis_complete/', views.siparis_complete, name = 'siparis_complete'),
]