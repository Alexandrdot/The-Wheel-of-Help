from django.urls import path, register_converter
from . import views
from .converter import RatingConverter

register_converter(RatingConverter, 'rating')

app_name = 'homepage'

urlpatterns = [
    # Главная
    path('', views.index, name='index'),
    
    # Категории (старые маршруты)
    path('tech-station/', views.technical_service_station, name='tech_station'),
    path('evacuators/', views.evacuator, name='evacuator'),
    path('tire-services/', views.tire_service, name='tire_service'),
    
    # ✅ НОВЫЙ УНИВЕРСАЛЬНЫЙ МАРШРУТ ДЛЯ КАТЕГОРИЙ (добавьте это)
    path('category/<slug:cat_slug>/', views.category_detail, name='category_detail'),
    
    # Поиск
    path('search/', views.search, name='search'),
    
    # Детальная страница (по слагу)
    path('service/<slug:service_slug>/', views.service_detail, name='service_detail'),
    
    # Фильтрация по рейтингу
    path('tech-station/rating/<rating:rating>/', views.rating_filter, name='tech_station_rating'),
    path('evacuators/rating/<rating:rating>/', views.rating_filter, name='evacuator_rating'),
    path('tire-services/rating/<rating:rating>/', views.rating_filter, name='tire_service_rating'),
]