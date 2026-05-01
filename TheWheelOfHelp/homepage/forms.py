from django import forms
from django.core.exceptions import ValidationError


# Собственный валидатор для проверки русских символов
def validate_russian(value):
    allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
    for char in value:
        if char not in allowed_chars:
            raise ValidationError("Допустимы только русские буквы, цифры, дефис и пробел")


# Форма, несвязанная с моделью (для обратной связи или поиска)
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ваше имя",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@mail.ru'})
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Ваше сообщение...'}),
        validators=[validate_russian]  # Собственный валидатор
    )
    
    # Собственный валидатор через метод clean_
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise ValidationError("Имя должно содержать минимум 2 символа")
        return name
    



from .models import CarService, Category


class CarServiceForm(forms.ModelForm):
    # Переопределяем поле с выбором категории
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Выберите категорию"
    )
    
    # Собственный валидатор для названия
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise ValidationError("Название должно содержать минимум 3 символа")
        if len(title) > 100:
            raise ValidationError("Название не должно превышать 100 символов")
        return title
    
    # Собственный валидатор для рейтинга
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise ValidationError("Рейтинг должен быть от 0 до 5")
        return rating
    
    class Meta:
        model = CarService
        fields = ['title', 'slug', 'category', 'description', 'address', 'phone', 'work_time', 'rating', 'is_published', 'tags', 'image']
        labels = {
            'title': 'Название СТО',
            'slug': 'URL (латиницей)',
            'description': 'Описание',
            'address': 'Адрес',
            'phone': 'Телефон',
            'work_time': 'Время работы',
            'rating': 'Рейтинг (0-5)',
            'is_published': 'Опубликовано',
            'tags': 'Теги',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'work_time': forms.TextInput(attrs={'class': 'form-input'}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Выберите файл",
        widget=forms.FileInput(attrs={'class': 'form-file'})
    )