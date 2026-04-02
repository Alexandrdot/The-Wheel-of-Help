from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Category, CarService, TireService, TowTruck, Status
from django.core.paginator import Paginator


def index(request):
    """Главная страница - показывает последние услуги из всех категорий"""
    # Получаем параметр фильтрации из GET-запроса
    rating_filter = request.GET.get('rating')
    
    # Объединяем все опубликованные услуги из трех моделей
    all_services = list(CarService.published.all()) + \
                   list(TireService.published.all()) + \
                   list(TowTruck.published.all())
    
    # Применяем фильтр по рейтингу если он указан
    if rating_filter:
        try:
            rating_filter = float(rating_filter)
            all_services = [s for s in all_services if s.rating >= rating_filter]
        except ValueError:
            pass
    
    # Сортируем по дате создания (новые сверху)
    all_services.sort(key=lambda x: x.time_create, reverse=True)

    # Пагинация: 10 услуг на странице
    paginator = Paginator(all_services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'homepage/index.html', {
        'title': 'Главная страница - Помощь на дорогах',
        'page_obj': page_obj,
        'categories': categories,
        'selected_cat_id': 0,
        'current_rating': rating_filter,  # Передаем текущий фильтр в шаблон
    })


def category_detail(request, cat_slug):
    """Универсальная страница для любой категории по слагу"""
    category = get_object_or_404(Category, slug=cat_slug)
    
    # Получаем параметр фильтрации из GET-запроса
    rating_filter = request.GET.get('rating')
    
    # Получаем услуги в зависимости от категории
    if category.slug == 'tech-station':  # СТО
        services = list(CarService.published.filter(category=category))
    elif category.slug == 'tire-services':  # Шиномонтаж
        services = list(TireService.published.filter(category=category))
    elif category.slug == 'evacuators':  # Эвакуаторы
        services = list(TowTruck.published.filter(category=category))
    else:
        services = []
    
    # Применяем фильтр по рейтингу если он указан
    if rating_filter:
        try:
            rating_filter = float(rating_filter)
            services = [s for s in services if s.rating >= rating_filter]
        except ValueError:
            pass
    
    # Сортируем по рейтингу (от лучшего к худшему)
    services.sort(key=lambda x: x.rating, reverse=True)

    return render(request, 'homepage/category_detail.html', {
        'title': category.name,
        'services': services,
        'category': category,
        'categories': Category.objects.all(),
        'selected_cat_id': category.id,
        'current_rating': rating_filter,  # Передаем текущий фильтр в шаблон
    })


def car_service_detail(request, service_slug):
    """Детальная страница СТО"""
    service = get_object_or_404(CarService, slug=service_slug, is_published=Status.PUBLISHED)
    return render(request, 'homepage/service_detail.html', {
        'service': service,
        'categories': Category.objects.all(),
        'selected_cat_id': service.category.id,
    })


def tire_service_detail(request, service_slug):
    """Детальная страница шиномонтажа"""
    service = get_object_or_404(TireService, slug=service_slug, is_published=Status.PUBLISHED)
    return render(request, 'homepage/service_detail.html', {
        'service': service,
        'categories': Category.objects.all(),
        'selected_cat_id': service.category.id,
    })


def tow_truck_detail(request, service_slug):
    """Детальная страница эвакуатора"""
    service = get_object_or_404(TowTruck, slug=service_slug, is_published=Status.PUBLISHED)
    return render(request, 'homepage/service_detail.html', {
        'service': service,
        'categories': Category.objects.all(),
        'selected_cat_id': service.category.id,
    })


def error_404(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")