from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('category/<slug:cat_slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('tech-station/<slug:service_slug>/', views.CarServiceDetailView.as_view(), name='car_service_detail'),
    path('tire-service/<slug:service_slug>/', views.TireServiceDetailView.as_view(), name='tire_service_detail'),
    path('tow-truck/<slug:service_slug>/', views.TowTruckDetailView.as_view(), name='tow_truck_detail'),

    path('add-service/', views.AddServiceChoiceView.as_view(), name='add_service'),
    path('add-service/car/', views.CarServiceCreateView.as_view(), name='add_car_service'),
    path('add-service/tire/', views.TireServiceCreateView.as_view(), name='add_tire_service'),
    path('add-service/tow/', views.TowTruckCreateView.as_view(), name='add_tow_truck'),

    path('car-service/<int:pk>/edit/', views.CarServiceUpdateView.as_view(), name='car_service_edit'),
    path('car-service/<int:pk>/delete/', views.CarServiceDeleteView.as_view(), name='car_service_delete'),
    path('tire-service/<int:pk>/edit/', views.TireServiceUpdateView.as_view(), name='tire_service_edit'),
    path('tire-service/<int:pk>/delete/', views.TireServiceDeleteView.as_view(), name='tire_service_delete'),
    path('tow-truck/<int:pk>/edit/', views.TowTruckUpdateView.as_view(), name='tow_truck_edit'),
    path('tow-truck/<int:pk>/delete/', views.TowTruckDeleteView.as_view(), name='tow_truck_delete'),

    path('tag/<slug:tag_slug>/', views.TagDetailView.as_view(), name='tag_detail'),

    path('react/', views.ServiceReactionView.as_view(), name='service_react'),

    path('search/', views.SearchView.as_view(), name='search'),

    path('contact/', views.ContactView.as_view(), name='contact'),

]
