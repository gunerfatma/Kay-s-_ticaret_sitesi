from django.urls import path
from .import views

urlpatterns = [
    path('', views.store, name ='store'),
    path('category/<slug:category_slug>/', views.store, name ='urunler_by_category'),
    path('category/<slug:category_slug>/<slug:urun_slug>/', views.urun_detail, name ='urun_detail'),
    path('search/', views.search, name = 'search'),
    path('sumbit_puan/<int:urun_id>/', views.sumbit_puan, name='sumbit_puan'),
]

  
   