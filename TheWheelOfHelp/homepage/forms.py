from django import forms
from django.core.exceptions import ValidationError

from .constants import CATEGORY_SLUG_STO, CATEGORY_SLUG_TIRE, CATEGORY_SLUG_TOW
from .models import CarService, Category, Status, Tag, TireService, TowTruck


class CommentForm(forms.Form):
    text = forms.CharField(
        label='Комментарий',
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-textarea',
                'id': 'id_comment_text',
                'rows': 3,
                'placeholder': 'Напишите комментарий...',
            },
        ),
    )


def validate_russian(value):
    allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
    for char in value:
        if char not in allowed_chars:
            raise ValidationError("Допустимы только русские буквы, цифры, дефис и пробел")


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ваше имя",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя'}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@mail.ru'}),
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Ваше сообщение...'}),
        validators=[validate_russian],
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise ValidationError("Имя должно содержать минимум 2 символа")
        return name


class BaseServiceForm(forms.ModelForm):
    category_slug = None

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        label="Категория",
        empty_label="Выберите категорию",
    )
    phone = forms.CharField(
        label="Телефон",
        min_length=10,
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    is_published = forms.BooleanField(
        label='Опубликовано (отображать на сайте)',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
    )

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise ValidationError("Название должно содержать минимум 3 символа")
        if len(title) > 100:
            raise ValidationError("Название не должно превышать 100 символов")
        return title

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise ValidationError("Рейтинг должен быть от 0 до 5")
        return rating

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['is_published'].initial = self.instance.is_published == Status.PUBLISHED
        if self.category_slug:
            qs = Category.objects.filter(slug=self.category_slug)
            self.fields['category'].queryset = qs
            if qs.count() == 1:
                if self.instance and self.instance.pk:
                    self.fields['category'].initial = self.instance.category_id
                else:
                    self.fields['category'].initial = qs.first().pk
                self.fields['category'].widget = forms.HiddenInput()

    class Meta:
        fields = [
            'title',
            'slug',
            'category',
            'description',
            'address',
            'phone',
            'work_time',
            'rating',
            'is_published',
            'tags',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Например: АвтоМастер на Ленина',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'avto-master-lenina',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 5,
                'placeholder': 'Кратко опишите услуги и преимущества',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ул. Примерная, 10',
            }),
            'work_time': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '09:00–21:00 или круглосуточно',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-input form-input--short',
                'step': '0.1',
                'min': '0',
                'max': '5',
            }),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class CarServiceForm(BaseServiceForm):
    category_slug = CATEGORY_SLUG_STO

    class Meta(BaseServiceForm.Meta):
        model = CarService
        fields = BaseServiceForm.Meta.fields + [
            'specialization',
            'diagnostic_available',
            'image',
        ]
        labels = {
            'title': 'Название',
            'slug': 'URL (латиницей)',
            'description': 'Описание',
            'address': 'Адрес',
            'work_time': 'Время работы',
            'rating': 'Рейтинг (0–5)',
            'is_published': 'Опубликовано',
            'tags': 'Теги',
            'specialization': 'Специализация',
            'diagnostic_available': 'Компьютерная диагностика',
            'image': 'Изображение',
        }
        widgets = {
            **BaseServiceForm.Meta.widgets,
            'specialization': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ремонт двигателей, ходовая часть…',
            }),
            'diagnostic_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
        }


class TireServiceForm(BaseServiceForm):
    category_slug = CATEGORY_SLUG_TIRE

    class Meta(BaseServiceForm.Meta):
        model = TireService
        fields = BaseServiceForm.Meta.fields + [
            'wheel_size_from',
            'wheel_size_to',
            'tire_storage',
        ]
        labels = {
            'title': 'Название',
            'slug': 'URL (латиницей)',
            'description': 'Описание',
            'address': 'Адрес',
            'work_time': 'Время работы',
            'rating': 'Рейтинг (0–5)',
            'is_published': 'Опубликовано',
            'tags': 'Теги',
            'wheel_size_from': 'Размер шин от (R)',
            'wheel_size_to': 'Размер шин до (R)',
            'tire_storage': 'Сезонное хранение',
        }
        widgets = {
            **BaseServiceForm.Meta.widgets,
            'wheel_size_from': forms.NumberInput(attrs={'class': 'form-input form-input--short'}),
            'wheel_size_to': forms.NumberInput(attrs={'class': 'form-input form-input--short'}),
            'tire_storage': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class TowTruckForm(BaseServiceForm):
    category_slug = CATEGORY_SLUG_TOW

    class Meta(BaseServiceForm.Meta):
        model = TowTruck
        fields = BaseServiceForm.Meta.fields + [
            'load_capacity',
            'work_24_7',
        ]
        labels = {
            'title': 'Название',
            'slug': 'URL (латиницей)',
            'description': 'Описание',
            'address': 'Адрес',
            'work_time': 'Время работы',
            'rating': 'Рейтинг (0–5)',
            'is_published': 'Опубликовано',
            'tags': 'Теги',
            'load_capacity': 'Грузоподъёмность (тонн)',
            'work_24_7': 'Круглосуточно',
        }
        widgets = {
            **BaseServiceForm.Meta.widgets,
            'load_capacity': forms.NumberInput(attrs={'class': 'form-input form-input--short'}),
            'work_24_7': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Выберите файл",
        widget=forms.FileInput(attrs={'class': 'form-file'}),
    )
