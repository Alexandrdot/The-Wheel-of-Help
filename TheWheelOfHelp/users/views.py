from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from homepage.models import CarService, TireService, TowTruck

from .forms import LoginUserForm, ProfileUserForm, RegisterUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('homepage:index')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        my_services = (
            list(CarService.objects.filter(author=user).select_related('category'))
            + list(TireService.objects.filter(author=user).select_related('category'))
            + list(TowTruck.objects.filter(author=user).select_related('category'))
        )
        my_services.sort(key=lambda service: service.time_create, reverse=True)
        context['title'] = 'Профиль пользователя'
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['my_services'] = my_services
        return context


class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Изменение пароля'}


class UserLogoutView(LogoutView):
    """Выход только через POST (требование Django 5+)."""

    http_method_names = ['post', 'options']
    next_page = reverse_lazy('homepage:index')

    def get_success_url(self):
        return reverse_lazy('homepage:index')
