from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView

from .constants import CATEGORY_SLUG_STO, CATEGORY_SLUG_TIRE, CATEGORY_SLUG_TOW
from .forms import CarServiceForm, ContactForm, TireServiceForm, TowTruckForm
from .interactions import set_reaction
from .mixins import (
    ServiceDeletePermissionMixin,
    ServiceEngagementDetailMixin,
    ServiceUpdatePermissionMixin,
    ServicesListEngagementMixin,
)
from .models import CarService, Category, ServiceReaction, Status, Tag, TireService, TowTruck
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


class IndexView(ServicesListEngagementMixin, DataMixin, ListView):
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


class CategoryDetailView(ServicesListEngagementMixin, DataMixin, ListView):
    template_name = 'homepage/category_detail.html'
    context_object_name = 'services'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])

    def get_queryset(self):
        cat = self._category
        if cat.slug == CATEGORY_SLUG_STO:
            services = list(CarService.published.filter(category=cat).select_related('category'))
        elif cat.slug == CATEGORY_SLUG_TIRE:
            services = list(TireService.published.filter(category=cat).select_related('category'))
        elif cat.slug == CATEGORY_SLUG_TOW:
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


def _service_detail_queryset(request, model):
    qs = model.objects.select_related('category')
    if not request.user.is_authenticated:
        return qs.filter(is_published=Status.PUBLISHED)
    if request.user.is_superuser or request.user.has_perm(
        f'homepage.change_{model._meta.model_name}'
    ):
        return qs
    return qs.filter(Q(is_published=Status.PUBLISHED) | Q(author=request.user))


class ServiceReactionView(LoginRequiredMixin, View):
    def post(self, request):
        next_url = request.POST.get('next') or reverse_lazy('homepage:index')
        ct_id = request.POST.get('content_type_id')
        object_id = request.POST.get('object_id')
        value_key = request.POST.get('value')

        if not ct_id or not object_id or value_key not in ('like', 'dislike'):
            return redirect(next_url)

        ct = get_object_or_404(ContentType, pk=ct_id)
        model = ct.model_class()
        if model not in (CarService, TireService, TowTruck):
            return redirect(next_url)

        service = get_object_or_404(model, pk=object_id)
        if not _service_detail_queryset(request, model).filter(pk=service.pk).exists():
            return redirect(next_url)

        reaction_value = (
            ServiceReaction.LIKE if value_key == 'like' else ServiceReaction.DISLIKE
        )
        set_reaction(request.user, service, reaction_value)
        return redirect(next_url)


class CarServiceDetailView(ServiceEngagementDetailMixin, DataMixin, DetailView):
    model = CarService
    template_name = 'homepage/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_queryset(self):
        return _service_detail_queryset(self.request, CarService)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=self.object.title,
            selected_cat_id=self.object.category_id,
        )


class TireServiceDetailView(ServiceEngagementDetailMixin, DataMixin, DetailView):
    model = TireService
    template_name = 'homepage/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_queryset(self):
        return _service_detail_queryset(self.request, TireService)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=self.object.title,
            selected_cat_id=self.object.category_id,
        )


class TowTruckDetailView(ServiceEngagementDetailMixin, DataMixin, DetailView):
    model = TowTruck
    template_name = 'homepage/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_queryset(self):
        return _service_detail_queryset(self.request, TowTruck)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=self.object.title,
            selected_cat_id=self.object.category_id,
        )


class TagDetailView(ServicesListEngagementMixin, DataMixin, ListView):
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


class AddServiceChoiceView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'homepage/add_service_choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Добавление услуги', selected_cat_id=0)


class _ServiceFormMixin(DataMixin):
    template_name = 'homepage/service_form.html'

    def get_success_url(self):
        if self.object.is_published:
            return self.object.get_absolute_url()
        return self.object.category.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.object.pk:
            self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_edit = bool(self.object and self.object.pk)
        cat_id = self.object.category_id if is_edit else 0
        return self.get_mixin_context(
            context,
            is_edit=is_edit,
            selected_cat_id=cat_id,
        )


class CarServiceCreateView(LoginRequiredMixin, _ServiceFormMixin, CreateView):
    model = CarService
    form_class = CarServiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление СТО'
        context['service_type_label'] = 'СТО'
        return context


class CarServiceUpdateView(ServiceUpdatePermissionMixin, _ServiceFormMixin, UpdateView):
    model = CarService
    form_class = CarServiceForm
    queryset = CarService.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование СТО'
        context['service_type_label'] = 'СТО'
        return context


class CarServiceDeleteView(ServiceDeletePermissionMixin, DataMixin, DeleteView):
    model = CarService
    template_name = 'homepage/service_confirm_delete.html'
    queryset = CarService.objects.all()
    success_url = reverse_lazy('homepage:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Удаление услуги',
            selected_cat_id=self.object.category_id,
        )


class TireServiceCreateView(LoginRequiredMixin, _ServiceFormMixin, CreateView):
    model = TireService
    form_class = TireServiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление шиномонтажа'
        context['service_type_label'] = 'Шиномонтаж'
        return context


class TireServiceUpdateView(ServiceUpdatePermissionMixin, _ServiceFormMixin, UpdateView):
    model = TireService
    form_class = TireServiceForm
    queryset = TireService.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование шиномонтажа'
        context['service_type_label'] = 'Шиномонтаж'
        return context


class TireServiceDeleteView(ServiceDeletePermissionMixin, DataMixin, DeleteView):
    model = TireService
    template_name = 'homepage/service_confirm_delete.html'
    queryset = TireService.objects.all()
    success_url = reverse_lazy('homepage:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Удаление услуги',
            selected_cat_id=self.object.category_id,
        )


class TowTruckCreateView(LoginRequiredMixin, _ServiceFormMixin, CreateView):
    model = TowTruck
    form_class = TowTruckForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление эвакуатора'
        context['service_type_label'] = 'Эвакуатор'
        return context


class TowTruckUpdateView(ServiceUpdatePermissionMixin, _ServiceFormMixin, UpdateView):
    model = TowTruck
    form_class = TowTruckForm
    queryset = TowTruck.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование эвакуатора'
        context['service_type_label'] = 'Эвакуатор'
        return context


class TowTruckDeleteView(ServiceDeletePermissionMixin, DataMixin, DeleteView):
    model = TowTruck
    template_name = 'homepage/service_confirm_delete.html'
    queryset = TowTruck.objects.all()
    success_url = reverse_lazy('homepage:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title='Удаление услуги',
            selected_cat_id=self.object.category_id,
        )



class SearchView(ServicesListEngagementMixin, DataMixin, ListView):
    """Поиск по названию и адресу среди всех опубликованных услуг."""

    template_name = 'homepage/search_results.html'

    def get(self, request, *args, **kwargs):
        if not request.GET.get('q', '').strip():
            return redirect(reverse_lazy('homepage:index'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip().lower()
        if not q:
            return []
        all_services = (
            list(CarService.published.select_related('category'))
            + list(TireService.published.select_related('category'))
            + list(TowTruck.published.select_related('category'))
        )
        services = [
            s for s in all_services
            if q in s.title.lower() or q in (s.address or '').lower()
        ]
        services.sort(key=lambda x: x.time_create, reverse=True)
        return services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        return self.get_mixin_context(
            context,
            title=f'Поиск: {q}' if q else 'Поиск',
            selected_cat_id=0,
            search_query=q,
        )


