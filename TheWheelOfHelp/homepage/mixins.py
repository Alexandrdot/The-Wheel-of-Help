from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

from .forms import CommentForm
from .permissions import user_can_change_service, user_can_delete_service
from .interactions import bulk_engagement, get_comments, set_reaction
from .models import Comment


class ServiceObjectPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Доступ к редактированию/удалению: автор записи или модератор с правами Django."""

    permission_action = 'change'

    def test_func(self):
        service = self.get_object()
        if self.permission_action == 'delete':
            return user_can_delete_service(self.request.user, service)
        return user_can_change_service(self.request.user, service)


class ServiceUpdatePermissionMixin(ServiceObjectPermissionMixin):
    permission_action = 'change'


class ServiceDeletePermissionMixin(ServiceObjectPermissionMixin):
    permission_action = 'delete'


class ServicesListEngagementMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = list(context.get('services', []))
        if not services and context.get('page_obj'):
            services = list(context['page_obj'])
        if services:
            bulk_engagement(services, self.request.user)
        return context


class ServiceEngagementDetailMixin:
    http_method_names = ['get', 'post', 'head', 'options']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        self.object = self.get_object()
        if request.POST.get('action') != 'comment':
            return redirect(self.object.get_absolute_url())
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=request.user,
                content_object=self.object,
                text=form.cleaned_data['text'],
            )
            return redirect(self.object.get_absolute_url())
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        bulk_engagement([service], self.request.user)
        context['comments'] = get_comments(service)
        context['comment_form'] = (
            CommentForm() if self.request.user.is_authenticated else None
        )
        return context
