from django.urls import path, register_converter
from . import views
from .converter import RatingConverter

register_converter(RatingConverter, 'rating')

app_name = 'homepage'

urlpatterns = [
    # Главная
    path('', views.index, name='index'),

    # Страница категории
    path('category/<slug:cat_slug>/', views.category_detail, name='category_detail'),

    # Детальные страницы для каждого типа услуги
    path('tech-station/<slug:service_slug>/', views.car_service_detail, name='car_service_detail'),
    path('tire-service/<slug:service_slug>/', views.tire_service_detail, name='tire_service_detail'),
    path('tow-truck/<slug:service_slug>/', views.tow_truck_detail, name='tow_truck_detail'),

    path('tag/<slug:tag_slug>/', views.tag_detail, name='tag_detail'),

    path('demo-orm/', views.demo_orm, name='demo_orm'),

]