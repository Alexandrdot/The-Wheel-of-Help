from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Category, CarService, TireService, TowTruck, Status, Tag
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


def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    
    # Получаем все услуги с этим тегом из трех таблиц
    services = []
    services += list(tag.car_services.filter(is_published=Status.PUBLISHED))
    services += list(tag.tire_services.filter(is_published=Status.PUBLISHED))
    services += list(tag.tow_trucks.filter(is_published=Status.PUBLISHED))
    
    return render(request, 'homepage/tag_detail.html', {
        'title': f'Тег: {tag.name}',
        'tag': tag,
        'services': services,
        'categories': Category.objects.all(),
    })


def demo_orm(request):
    """Демонстрация методов ORM из лабораторной работы №8"""

    results = {}
    
    # ========== 1. МЕТОДЫ ВЫБОРА ЗАПИСЕЙ (из текста) ==========
    # first() - первая запись
    results['first'] = CarService.objects.first()
    
    # last() - последняя запись
    results['last'] = CarService.objects.last()
    
    # order_by() - сортировка
    results['order_by_asc'] = CarService.objects.order_by("rating")[:3]
    results['order_by_desc'] = CarService.objects.order_by("-rating")[:3]
    
    # filter() - фильтрация
    results['filter'] = CarService.objects.filter(rating__gte=4.0)
    
    # exclude() - исключить
    results['exclude'] = CarService.objects.exclude(rating__lt=4.0)
    
    # get() - получить одну запись
    try:
        results['get'] = CarService.objects.get(pk=1)
    except:
        results['get'] = None
    
    # latest() и earliest() - по дате
    results['latest'] = CarService.objects.latest("time_update")
    results['earliest'] = CarService.objects.earliest("time_update")
    
    # get_previous_by_ и get_next_by_ (если есть запись)
    last_service = CarService.objects.last()
    if last_service:
        try:
            results['previous'] = last_service.get_previous_by_time_update()
        except:
            results['previous'] = None
        try:
            results['next'] = last_service.get_next_by_time_update()
        except:
            results['next'] = None
    
    # exists() - проверка существования
    results['exists'] = CarService.objects.filter(rating__gt=4.5).exists()
    
    # count() - количество записей
    results['count'] = CarService.objects.count()
    
    # ========== 2. КЛАСС Q (из текста) ==========
    from django.db.models import Q
    
    # Q с OR (логическое ИЛИ)
    results['q_or'] = CarService.objects.filter(
        Q(rating__lt=5) | Q(diagnostic_available=True)
    )[:5]
    
    # Q с AND (логическое И)
    results['q_and'] = CarService.objects.filter(
        Q(rating__lt=5) & Q(diagnostic_available=True)
    )[:5]
    
    # Q с NOT (логическое НЕ)
    results['q_not'] = CarService.objects.filter(
        ~Q(rating__lt=4)
    )[:5]
    
    # Комбинация Q с обычными аргументами
    results['q_combined'] = CarService.objects.filter(
        Q(rating__gt=4.0) | Q(diagnostic_available=True),
        is_published=1
    )[:5]
    
    # ========== 3. КЛАСС F (из текста) ==========
    from django.db.models import F
    
    # F в annotate - увеличение рейтинга
    results['f_annotate'] = CarService.objects.annotate(
        rating_plus = F('rating') + 0.5
    )[:5]
    
    # F в update - обновление (показываем без сохранения)
    results['f_update_demo'] = "F('rating') + 1 увеличит рейтинг на 1"
    
    # ========== 4. КЛАСС Value (из текста) ==========
    from django.db.models import Value
    
    results['value_annotate'] = CarService.objects.annotate(
        is_tr = Value(True),
        status = Value("Активно")
    )[:5]
    
    # ========== 5. МЕТОД annotate() (из текста) ==========
    results['annotate'] = CarService.objects.annotate(
        work_age = F('rating') * 2
    )[:5]
    
    # ========== 6. АГРЕГИРУЮЩИЕ ФУНКЦИИ (из текста) ==========
    from django.db.models import Count, Sum, Avg, Max, Min
    
    # aggregate с Min, Max
    results['aggregate_min_max'] = CarService.objects.aggregate(
        min_rating = Min('rating'),
        max_rating = Max('rating')
    )
    
    # aggregate с несколькими функциями
    results['aggregate_several'] = CarService.objects.aggregate(
        young = Min('rating'),
        old = Max('rating'),
        avg_rating = Avg('rating'),
        sum_rating = Sum('rating')
    )
    
    # aggregate с фильтром
    results['aggregate_filtered'] = CarService.objects.filter(
        pk__gt=1
    ).aggregate(
        res = Count('id')
    )
    
    # ========== 7. ГРУППИРОВКА ЗАПИСЕЙ (из текста) ==========
    # values + annotate + Count
    results['group_by'] = CarService.objects.values('category__name').annotate(
        total = Count('id')
    )
    
    # annotate + filter (total__gt=0)
    results['group_filter'] = Category.objects.annotate(
        total = Count('car_services')
    ).filter(total__gt=0)
    
    # ========== 8. ВЫЧИСЛЕНИЯ НА СТОРОНЕ СУБД (из текста) ==========
    from django.db.models.functions import Length
    
    results['db_length'] = CarService.objects.annotate(
        len_name = Length('title')
    )[:5]

    return render(request, 'homepage/demo_orm.html', {'results': results})