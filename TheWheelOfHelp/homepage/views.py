from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound 
from .models import Category, Service, Status  # 👈 1. ДОБАВЛЯЕМ Status В ИМПОРТ

def index(request):
    """Главная страница"""
    services = Service.published.all()
    categories = Category.objects.all()
    
    return render(request, 'homepage/index.html', {
        'title': 'Главная страница',
        'services': services,
        'categories': categories,
    })

def technical_service_station(request):
    """Страница со списком СТО"""
    category = get_object_or_404(Category, slug='tech-station')
    services = Service.published.filter(category=category)
    
    return render(request, 'homepage/tech_station.html', {
        'title': 'СТО',
        'services': services,
        'categories': Category.objects.all(),
        'selected_cat_id': category.id,
    })

def evacuator(request):
    """Страница с эвакуаторами"""
    category = get_object_or_404(Category, slug='evacuators')
    services = Service.published.filter(category=category)
    
    return render(request, 'homepage/evacuator.html', {
        'title': 'Эвакуаторы',
        'services': services,
        'categories': Category.objects.all(),
        'selected_cat_id': category.id,
    })

def tire_service(request):
    """Страница с шиномонтажом"""
    category = get_object_or_404(Category, slug='tire-services')
    services = Service.published.filter(category=category)
    
    return render(request, 'homepage/tire_service.html', {
        'title': 'Шиномонтаж',
        'services': services,
        'categories': Category.objects.all(),
        'selected_cat_id': category.id,
    })

def service_detail(request, service_slug):
    """Детальная страница услуги"""
    # 👇 2. ИСПРАВЛЯЕМ: Status.PUBLISHED вместо Service.Status.PUBLISHED
    service = get_object_or_404(
        Service, 
        slug=service_slug, 
        is_published=Status.PUBLISHED  # 👈 УБРАЛИ Service.
    )
    
    # Выбираем шаблон по категории
    template_map = {
        'tech-station': 'homepage/open_tech_station.html',
        'evacuators': 'homepage/open_evacuator.html',
        'tire-services': 'homepage/open_tire_service.html',
    }
    
    template = template_map.get(service.category.slug, 'homepage/service_detail.html')
    
    return render(request, template, {
        'service': service,
        'categories': Category.objects.all(),
        'selected_cat_id': service.category.id,
    })

def search(request):
    """Поиск по услугам"""
    query = request.GET.get('q', '')
    
    if query:
        services = Service.published.filter(
            title__icontains=query
        ) | Service.published.filter(
            description__icontains=query
        )
    else:
        services = Service.published.none()
    
    return render(request, 'homepage/search.html', {
        'query': query,
        'results': services,
        'categories': Category.objects.all(),
    })

def rating_filter(request, rating):
    """Фильтрация услуг по рейтингу"""
    url_name = request.resolver_match.url_name
    
    category_map = {
        'tech_station_rating': 'tech-station',
        'evacuator_rating': 'evacuators',
        'tire_service_rating': 'tire-services',
    }
    
    category_slug = category_map.get(url_name)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        services = Service.published.filter(
            category=category,
            rating__gte=rating
        )
        title = f"{category.name} с рейтингом {rating}+"
        selected_cat = category.id
    else:
        services = Service.published.filter(rating__gte=rating)
        title = f"Услуги с рейтингом {rating}+"
        selected_cat = None
    
    if rating >= 4.8:
        rating_text = "Отличный"
    elif rating >= 4.0:
        rating_text = "Хороший"
    elif rating >= 3.0:
        rating_text = "Неплохой"
    else:
        rating_text = "Средний"
    
    return render(request, 'homepage/rating.html', {
        'services': services,
        'rating': rating,
        'rating_text': rating_text,
        'title': title,
        'categories': Category.objects.all(),
        'selected_cat_id': selected_cat,
    })

def error_404(request, exception):
    return HttpResponseNotFound("Error 404")

def category_detail(request, cat_slug):
    """Универсальная страница для любой категории по слагу"""
    category = get_object_or_404(Category, slug=cat_slug)
    services = Service.published.filter(category=category)
    
    return render(request, 'homepage/category_detail.html', {
        'title': category.name,
        'services': services,
        'category': category,
        'categories': Category.objects.all(),
        'selected_cat_id': category.id,
    })