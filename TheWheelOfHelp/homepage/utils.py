from .models import Category


class DataMixin:
    """Общий контекст (сайдбар) и настройки пагинации для CBV."""

    paginate_by = 5

    def get_mixin_context(self, context, **kwargs):
        context['categories'] = Category.objects.all()
        context.update(kwargs)
        return context
