from .import views
from django.urls import path

urlpatterns = [
    path('', views.kart, name='kart'),
    path('add_kart/<int:urun_id>/', views.add_kart, name='add_kart'),
    path('remove_kart/<int:urun_id>/<int:kart_item_id>/', views.remove_kart, name='remove_kart'),
    path('remove_kart_item/<int:urun_id>/<int:kart_item_id>/', views.remove_kart_item, name='remove_kart_item'),

    path('checkout/', views.checkout, name='checkout'),
]
