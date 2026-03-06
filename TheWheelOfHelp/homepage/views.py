# from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseNotFound

# # Create your views here.

# def error_404(request, exception):
#     return HttpResponseNotFound("Error 404")


# def index(request):
#     return HttpResponse('HomePage')


# def technical_service_station(request):
#     return HttpResponse('СТО')


# def evacuator(request):
#     name = request.GET.get('name', ' ')
#     return HttpResponse(f'Эвакуаторы {name}')


# def tire_service(request):
#     return HttpResponse('Шиномонтаж')


# def search(request):
#     return redirect('homepage:index')


# def open_tech_station(request, id):
#     return HttpResponse(f'СТО {id}')


# def open_evacuator(request, id):
#     return HttpResponse(f'Эвакуатор {id}')


# def open_tire_service(request, id):
#     return HttpResponse(f'Шиномонтаж {id}')


# def rating(request, rating):
#     if rating >= 4.8:
#         category = "Отличный"
#     elif rating >= 4.0:
#         category = "Хороший"
#     elif rating >= 3.0:
#         category = "Неплохой"
#     elif rating >= 2.0:
#         category = "Средний"
#     else:
#         category = "Плохой"

#     return HttpResponse(f"<h1>{category}<h1>")
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.

def error_404(request, exception):
    return HttpResponseNotFound("Error 404")

def index(request):
    """Главная страница со всеми услугами"""
    data = {
        'title': 'Главная страница'
    }
    return render(request, 'homepage/index.html', context=data)

def technical_service_station(request):
    """Страница со списком СТО"""
    data = {
        'title': 'Станции технического обслуживания',
        'service_type': 'СТО',
    }
    return render(request, 'homepage/tech_station.html', context=data)

def evacuator(request):
    """Страница со списком эвакуаторов"""
    name = request.GET.get('name', '')
    data = {
        'title': 'Эвакуаторы',
        'service_type': 'Эвакуаторы',
        'search_name': name,
    }
    return render(request, 'homepage/evacuator.html', context=data)

def tire_service(request):
    """Страница со списком шиномонтажей"""
    data = {
        'title': 'Шиномонтаж',
        'service_type': 'Шиномонтаж',
    }
    return render(request, 'homepage/tire_service.html', context=data)

def search(request):
    """Страница результатов поиска"""
    query = request.GET.get('q', '')
    # Здесь будет логика поиска
    results = []  # Заглушка
    data = {
        'query': query,
        'results': results,
    }
    return render(request, 'homepage/search.html', context=data)

def open_tech_station(request, id):
    """Детальная страница СТО"""
    data = {
        'id': id,
        'title': f'СТО #{id}',
    }
    return render(request, 'homepage/open_tech_station.html', context=data)

def open_evacuator(request, id):
    """Детальная страница эвакуатора"""
    data = {
        'id': id,
        'title': f'Эвакуатор #{id}',
    }
    return render(request, 'homepage/open_evacuator.html', context=data)

def open_tire_service(request, id):
    """Детальная страница шиномонтажа"""
    data = {
        'id': id,
        'title': f'Шиномонтаж #{id}',
    }
    return render(request, 'homepage/open_tire_service.html', context=data)

def rating(request, rating):
    """Страница с фильтрацией по рейтингу"""
    # Определяем категорию рейтинга
    if rating >= 4.8:
        category = "Отличный"
    elif rating >= 4.0:
        category = "Хороший"
    elif rating >= 3.0:
        category = "Неплохой"
    elif rating >= 2.0:
        category = "Средний"
    else:
        category = "Плохой"
    
    # Определяем текущий сервис из URL
    service_url = request.resolver_match.url_name
    service_name = {
        'tech_station_rating': 'СТО',
        'evacuator_rating': 'Эвакуаторы',
        'tire_service_rating': 'Шиномонтаж',
    }.get(service_url, 'Услуги')
    
    data = {
        'rating': rating,
        'rating_category': category,
        'service_name': service_name,
        'service_url': service_url.replace('_rating', ''),
        'category_name': f'{service_name} с рейтингом {rating}+',
    }
    return render(request, 'homepage/rating.html', context=data)