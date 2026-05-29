from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Status.PUBLISHED)


class BaseService(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    work_time = models.CharField(max_length=255, blank=True, verbose_name="Время работы")
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(class)s_authored',
        null=True,
        blank=True,
        verbose_name='Автор',
    )
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        abstract = True
        ordering = ['-time_create']
    
    def __str__(self):
        return self.title

    def change_permission(self):
        return f'{self._meta.app_label}.change_{self._meta.model_name}'

    def delete_permission(self):
        return f'{self._meta.app_label}.delete_{self._meta.model_name}'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('homepage:category_detail', kwargs={'cat_slug': self.slug})
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('homepage:tag_detail', kwargs={'tag_slug': self.slug})
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class ContactInfo(models.Model):
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Сайт")
    social_vk = models.URLField(blank=True, verbose_name="ВКонтакте")
    social_tg = models.URLField(blank=True, verbose_name="Telegram")
    
    def __str__(self):
        return f"Контакты: {self.email if self.email else 'не указаны'}"
    
    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"


class CarService(BaseService):
    specialization = models.CharField(max_length=200, blank=True, verbose_name="Специализация")
    diagnostic_available = models.BooleanField(default=True, verbose_name="Компьютерная диагностика")
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", related_name='car_services')
    tags = models.ManyToManyField(Tag, blank=True, related_name='car_services', verbose_name="Теги")
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='car_service', verbose_name="Контакты")
    image = models.ImageField(
        upload_to='services/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    class Meta:
        verbose_name = "СТО"
        verbose_name_plural = "СТО"
    
    def get_absolute_url(self):
        return reverse('homepage:car_service_detail', kwargs={'service_slug': self.slug})

    def get_edit_url(self):
        return reverse('homepage:car_service_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('homepage:car_service_delete', kwargs={'pk': self.pk})


class TireService(BaseService):
    wheel_size_from = models.IntegerField(default=13, verbose_name="Размер шин от")
    wheel_size_to = models.IntegerField(default=22, verbose_name="Размер шин до")
    tire_storage = models.BooleanField(default=False, verbose_name="Сезонное хранение")
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", related_name='tire_services')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tire_services', verbose_name="Теги")
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='tire_service', verbose_name="Контакты")
    
    class Meta:
        verbose_name = "Шиномонтаж"
        verbose_name_plural = "Шиномонтаж"
    
    def get_absolute_url(self):
        return reverse('homepage:tire_service_detail', kwargs={'service_slug': self.slug})

    def get_edit_url(self):
        return reverse('homepage:tire_service_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('homepage:tire_service_delete', kwargs={'pk': self.pk})


class TowTruck(BaseService):
    load_capacity = models.IntegerField(default=2, verbose_name="Грузоподъемность (тонн)")
    work_24_7 = models.BooleanField(default=False, verbose_name="Круглосуточно")
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", related_name='tow_trucks')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tow_trucks', verbose_name="Теги")
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='tow_truck', verbose_name="Контакты")
    
    class Meta:
        verbose_name = "Эвакуатор"
        verbose_name_plural = "Эвакуаторы"
    
    def get_absolute_url(self):
        return reverse('homepage:tow_truck_detail', kwargs={'service_slug': self.slug})

    def get_edit_url(self):
        return reverse('homepage:tow_truck_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('homepage:tow_truck_delete', kwargs={'pk': self.pk})


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_comments',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']

    def __str__(self):
        return f'{self.author}: {self.text[:40]}'


class ServiceReaction(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = (
        (LIKE, 'Нравится'),
        (DISLIKE, 'Не нравится'),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_reactions',
        verbose_name='Пользователь',
    )
    value = models.SmallIntegerField(choices=VALUE_CHOICES, verbose_name='Оценка')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Реакция'
        verbose_name_plural = 'Реакции'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'content_type', 'object_id'],
                name='unique_user_service_reaction',
            ),
        ]

    def __str__(self):
        label = 'лайк' if self.value == self.LIKE else 'дизлайк'
        return f'{self.user} — {label}'