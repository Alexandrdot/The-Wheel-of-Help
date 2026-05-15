import uuid
from django.db.models import Avg, Count, F, Max, Min, Q, Sum, Value
from django.db.models.functions import Length
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CarServiceForm, ContactForm, UploadFileForm
from .models import CarService, Category, Status, Tag, TireService, TowTruck
from .utils import DataMixin


def error_404(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def _parse_rating(get_value):
    if not get_value:
        return None
    try:
        return float(get_value)
    except ValueError:
        return None


def _merge_published_services():
    return (
        list(CarService.published.select_related('category'))
        + list(TireService.published.select_related('category'))
        + list(TowTruck.published.select_related('category'))
    )


class IndexView(DataMixin, ListView):
    """Главная: объединённый список услуг + фильтр по рейтингу + пагинация."""

    template_name = 'homepage/index.html'

    def get_queryset(self):
        services = _merge_published_services()
        rating = _parse_rating(self.request.GET.get('rating'))
        if rating is not None:
            services = [s for s in services if s.rating >= rating]
        services.sort(key=lambda x: x.time_create, reverse=True)
        return services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating_raw = self.request.GET.get('rating')
        current_rating = _parse_rating(rating_raw) if rating_raw else None
        return self.get_mixin_context(
            context,
            title='Главная страница - Помощь на дорогах',
            selected_cat_id=0,
            current_rating=current_rating,
        )


class CategoryDetailView(DataMixin, ListView):
    template_name = 'homepage/category_detail.html'
    context_object_name = 'services'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])

    def get_queryset(self):
        cat = self._category
        if cat.slug == 'tech-station':
            services = list(CarService.published.filter(category=cat).select_related('category'))
        elif cat.slug == 'tire-services':
            services = list(TireService.published.filter(category=cat).select_related('category'))
        elif cat.slug == 'evacuators':
            services = list(TowTruck.published.filter(category=cat).select_related('category'))
        else:
            services = []

        rating = _parse_rating(self.request.GET.get('rating'))
        if rating is not None:
            services = [s for s in services if s.rating >= rating]
        services.sort(key=lambda x: x.rating, reverse=True)
        return services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating_raw = self.request.GET.get('rating')
        current_rating = _parse_rating(rating_raw) if rating_raw else None
        return self.get_mixin_context(
            context,
            title=self._category.name,
            selected_cat_id=self._category.id,
            current_rating=current_rating,
        )


class CarServiceDetailView(DataMixin, DetailView):
    model = CarService
    template_name = 'homepage/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_queryset(self):
        return CarService.published.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=self.object.title,
            selected_cat_id=self.object.category_id,
            show_admin_actions=True,
        )


class TireServiceDetailView(DataMixin, DetailView):
    model = TireService
    template_name = 'homepage/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_queryset(self):
        return TireService.published.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=self.object.title,
            selected_cat_id=self.object.category_id,
            show_admin_actions=False,
        )


class TowTruckDetailView(DataMixin, DetailView):
    model = TowTruck
    template_name = 'homepage/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_queryset(self):
        return TowTruck.published.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=self.object.title,
            selected_cat_id=self.object.category_id,
            show_admin_actions=False,
        )


class TagDetailView(DataMixin, ListView):
    template_name = 'homepage/tag_detail.html'
    context_object_name = 'services'
    allow_empty = True

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])

    def get_queryset(self):
        tag = self._tag
        services = []
        services += list(tag.car_services.filter(is_published=Status.PUBLISHED).select_related('category'))
        services += list(tag.tire_services.filter(is_published=Status.PUBLISHED).select_related('category'))
        services += list(tag.tow_trucks.filter(is_published=Status.PUBLISHED).select_related('category'))
        return services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f'Тег: {self._tag.name}',
            selected_cat_id=0,
            tag=self._tag,
        )


class DemoOrmView(DataMixin, TemplateView):
    template_name = 'homepage/demo_orm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = {}

        results['first'] = CarService.objects.first()
        results['last'] = CarService.objects.last()
        results['order_by_asc'] = CarService.objects.order_by('rating')[:3]
        results['order_by_desc'] = CarService.objects.order_by('-rating')[:3]
        results['filter'] = CarService.objects.filter(rating__gte=4.0)
        results['exclude'] = CarService.objects.exclude(rating__lt=4.0)
        try:
            results['get'] = CarService.objects.get(pk=1)
        except CarService.DoesNotExist:
            results['get'] = None
        try:
            results['latest'] = CarService.objects.latest('time_update')
        except CarService.DoesNotExist:
            results['latest'] = None
        try:
            results['earliest'] = CarService.objects.earliest('time_update')
        except CarService.DoesNotExist:
            results['earliest'] = None

        last_service = CarService.objects.last()
        if last_service:
            try:
                results['previous'] = last_service.get_previous_by_time_update()
            except CarService.DoesNotExist:
                results['previous'] = None
            try:
                results['next'] = last_service.get_next_by_time_update()
            except CarService.DoesNotExist:
                results['next'] = None
        else:
            results['previous'] = results['next'] = None

        results['exists'] = CarService.objects.filter(rating__gt=4.5).exists()
        results['count'] = CarService.objects.count()

        results['q_or'] = CarService.objects.filter(Q(rating__lt=5) | Q(diagnostic_available=True))[:5]
        results['q_and'] = CarService.objects.filter(Q(rating__lt=5) & Q(diagnostic_available=True))[:5]
        results['q_not'] = CarService.objects.filter(~Q(rating__lt=4))[:5]
        results['q_combined'] = CarService.objects.filter(
            Q(rating__gt=4.0) | Q(diagnostic_available=True),
            is_published=1,
        )[:5]

        results['f_annotate'] = CarService.objects.annotate(rating_plus=F('rating') + 0.5)[:5]
        results['f_update_demo'] = "F('rating') + 1 увеличит рейтинг на 1"

        results['value_annotate'] = CarService.objects.annotate(is_tr=Value(True), status=Value('Активно'))[:5]
        results['annotate'] = CarService.objects.annotate(work_age=F('rating') * 2)[:5]

        results['aggregate_min_max'] = CarService.objects.aggregate(
            min_rating=Min('rating'),
            max_rating=Max('rating'),
        )
        results['aggregate_several'] = CarService.objects.aggregate(
            young=Min('rating'),
            old=Max('rating'),
            avg_rating=Avg('rating'),
            sum_rating=Sum('rating'),
        )
        results['aggregate_filtered'] = CarService.objects.filter(pk__gt=1).aggregate(res=Count('id'))
        results['group_by'] = CarService.objects.values('category__name').annotate(total=Count('id'))
        results['group_filter'] = Category.objects.annotate(total=Count('car_services')).filter(total__gt=0)
        results['db_length'] = CarService.objects.annotate(len_name=Length('title'))[:5]

        return self.get_mixin_context(
            context,
            title='Демонстрация ORM',
            selected_cat_id=0,
            results=results,
        )


class ContactView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'homepage/contact.html'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        print(f"От {name} ({email}): {message}")
        ctx = self.get_mixin_context({'name': name}, title='Сообщение отправлено', selected_cat_id=0)
        return render(self.request, 'homepage/contact_success.html', ctx)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Обратная связь', selected_cat_id=0)


class AddServiceView(DataMixin, CreateView):
    form_class = CarServiceForm
    template_name = 'homepage/add_service.html'
    success_url = reverse_lazy('homepage:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Добавление услуги', selected_cat_id=0)


class CarServiceUpdateView(DataMixin, UpdateView):
    model = CarService
    form_class = CarServiceForm
    template_name = 'homepage/add_service.html'
    success_url = reverse_lazy('homepage:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Редактирование услуги',
            selected_cat_id=self.object.category_id,
        )


class CarServiceDeleteView(DataMixin, DeleteView):
    model = CarService
    template_name = 'homepage/car_service_confirm_delete.html'
    success_url = reverse_lazy('homepage:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Удаление услуги',
            selected_cat_id=self.object.category_id,
        )


def handle_uploaded_file(f):
    ext = ''
    if '.' in f.name:
        ext = f.name[f.name.rindex('.'):]
        name = f.name[: f.name.rindex('.')]
    else:
        name = f.name

    unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"

    with open(f'media/uploads/{unique_name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return unique_name


class UploadFileView(DataMixin, View):
    def get(self, request):
        form = UploadFileForm()
        ctx = self.get_mixin_context({'form': form}, title='Загрузка файла', selected_cat_id=0)
        return render(request, 'homepage/upload.html', ctx)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            filename = handle_uploaded_file(uploaded_file)
            ctx = self.get_mixin_context({'filename': filename}, title='Файл загружен', selected_cat_id=0)
            return render(request, 'homepage/upload_success.html', ctx)
        ctx = self.get_mixin_context({'form': form}, title='Загрузка файла', selected_cat_id=0)
        return render(request, 'homepage/upload.html', ctx)
