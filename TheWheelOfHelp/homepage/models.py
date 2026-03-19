from django.db import models
from django.urls import reverse

# Модель для категорий (СТО, Эвакуаторы, Шиномонтаж)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('homepage:category_detail', kwargs={'cat_slug': self.slug})
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


# Класс-перечисление для статуса публикации
class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'      # 0 = черновик
    PUBLISHED = 1, 'Опубликовано'  # 1 = опубликовано


# Специальный менеджер для получения только опубликованных записей
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Status.PUBLISHED)


# Модель для услуг
class Service(models.Model):
    # Основные поля
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # Связь с категорией (один ко многим)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    
    # Контактные данные
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    work_time = models.CharField(max_length=255, blank=True, verbose_name="Время работы")
    
    # Рейтинг
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    
    # Дата создания и обновления (заполняются автоматически)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    # Статус публикации (используем перечисление)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    
    # Менеджеры для работы с записями
    objects = models.Manager()  # стандартный менеджер (все записи)
    published = PublishedManager()  # наш менеджер (только опубликованные)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('homepage:service_detail', kwargs={'service_slug': self.slug})
    
    class Meta:
        ordering = ['-time_create']  # сортировка по умолчанию (новые сверху)
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"