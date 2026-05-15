from django.urls import path, register_converter
from . import views
from .converter import RatingConverter

register_converter(RatingConverter, 'rating')

app_name = 'homepage'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('category/<slug:cat_slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('tech-station/<slug:service_slug>/', views.CarServiceDetailView.as_view(), name='car_service_detail'),
    path('tire-service/<slug:service_slug>/', views.TireServiceDetailView.as_view(), name='tire_service_detail'),
    path('tow-truck/<slug:service_slug>/', views.TowTruckDetailView.as_view(), name='tow_truck_detail'),

    path(
        'car-service/<int:pk>/edit/',
        views.CarServiceUpdateView.as_view(),
        name='car_service_edit',
    ),
    path(
        'car-service/<int:pk>/delete/',
        views.CarServiceDeleteView.as_view(),
        name='car_service_delete',
    ),

    path('tag/<slug:tag_slug>/', views.TagDetailView.as_view(), name='tag_detail'),

    path('demo-orm/', views.DemoOrmView.as_view(), name='demo_orm'),

    path('contact/', views.ContactView.as_view(), name='contact'),

    path('add-service/', views.AddServiceView.as_view(), name='add_service'),

    path('upload/', views.UploadFileView.as_view(), name='upload'),

]