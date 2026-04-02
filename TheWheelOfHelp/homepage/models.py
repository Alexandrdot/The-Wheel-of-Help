from django.db import models
from django.urls import reverse


# Класс-перечисление для статуса публикации
class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'


# Специальный менеджер для получения только опубликованных записей
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Status.PUBLISHED)


# Абстрактная базовая модель для всех видов услуг
class BaseService(models.Model):
    """Абстрактная модель с общими полями для СТО, эвакуаторов и шиномонтажа"""
    title = models.CharField(max_length=255, verbose_name="Название организации")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")

    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    work_time = models.CharField(max_length=255, blank=True, verbose_name="Время работы")

    rating = models.FloatField(default=0, verbose_name="Рейтинг (0-5)")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")

    # Менеджеры
    objects = models.Manager()  # стандартный менеджер (все записи)
    published = PublishedManager()  # наш менеджер (только опубликованные)

    class Meta:
        abstract = True  # Это абстрактная модель, таблица в БД не создается
        ordering = ['-time_create']
        verbose_name = "Базовая услуга"
        verbose_name_plural = "Базовые услуги"

    def __str__(self):
        return self.title


# Модель для категорий (СТО, Эвакуаторы, Шиномонтаж)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('homepage:category_detail', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


# --- Конкретные модели услуг, наследуемые от BaseService ---

class CarService(BaseService):
    """Модель для СТО (добавляем специфичные поля)"""
    # Специфичные поля для СТО
    specialization = models.CharField(max_length=200, blank=True, verbose_name="Специализация (ремонт двигателей, ходовой и т.д.)")
    diagnostic_available = models.BooleanField(default=True, verbose_name="Компьютерная диагностика")
    # Связь с категорией (один ко многим)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", related_name='car_services')

    class Meta:
        verbose_name = "СТО"
        verbose_name_plural = "СТО"

    def get_absolute_url(self):
        # URL для детальной страницы СТО
        return reverse('homepage:car_service_detail', kwargs={'service_slug': self.slug})


class TireService(BaseService):
    """Модель для шиномонтажа (добавляем специфичные поля)"""
    # Специфичные поля для шиномонтажа
    wheel_size_from = models.IntegerField(default=13, verbose_name="Размер шин от (R)")
    wheel_size_to = models.IntegerField(default=22, verbose_name="Размер шин до (R)")
    tire_storage = models.BooleanField(default=False, verbose_name="Сезонное хранение шин")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", related_name='tire_services')

    class Meta:
        verbose_name = "Шиномонтаж"
        verbose_name_plural = "Шиномонтаж"

    def get_absolute_url(self):
        return reverse('homepage:tire_service_detail', kwargs={'service_slug': self.slug})


class TowTruck(BaseService):
    """Модель для эвакуатора (добавляем специфичные поля)"""
    # Специфичные поля для эвакуатора
    load_capacity = models.IntegerField(default=2, verbose_name="Грузоподъемность (тонн)")
    work_24_7 = models.BooleanField(default=False, verbose_name="Круглосуточно")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", related_name='tow_trucks')

    class Meta:
        verbose_name = "Эвакуатор"
        verbose_name_plural = "Эвакуаторы"

    def get_absolute_url(self):
        return reverse('homepage:tow_truck_detail', kwargs={'service_slug': self.slug})