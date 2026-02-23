from django.urls import path, register_converter

from . import views
from .converter import RatingConverter

register_converter(RatingConverter, 'rating')

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'), # Главная (все записи)
    path('tech_station/', views.technical_service_station, name='tech_station'), # СТО (все записи)
    path('evacuator/', views.evacuator, name='evacuator'), # Эвакуаторы (все записи)
    path('tire_service/', views.tire_service, name='tire_service'), # Шиномонтаж (все записи)

    path('search/', views.search, name='search'), # Поиск (в верхней части)

    path('tech_station/<int:id>/', views.open_tech_station, name='open_tech_station'),
    path('evacuator/<int:id>/', views.open_evacuator, name='open_evacuator'),
    path('tire_service/<int:id>/', views.open_tire_service, name='open_tire_service'),

    path('tech_station/rating/<rating:rating>/', views.rating, name='tech_station_rating'),
    path('evacuator/rating/<rating:rating>/', views.rating, name='evacuator_rating'),
    path('tire_service/rating/<rating:rating>/', views.rating, name='tire_service_rating'),

]

# СТО Шиномонтаж Эвакуаторы
