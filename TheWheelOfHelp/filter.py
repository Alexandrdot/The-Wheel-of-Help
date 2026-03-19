# step3_filter.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheWheelOfHelp.settings')
django.setup()

from homepage.models import Category, Service, Status

print("=" * 60)
print("ЭТАП 3: ФИЛЬТРАЦИЯ ЗАПИСЕЙ (FILTER)")
print("=" * 60)

# 1. Фильтр по категории
print("\n1. Фильтр по категории (filter(category=...)):")
cat_sto = Category.objects.get(slug='tech-station')
sto_services = Service.objects.filter(category=cat_sto)
print(f"   Услуги в категории 'СТО': {sto_services.count()}")
for s in sto_services:
    print(f"   - {s.title}")

# 2. Фильтр по рейтингу (больше или равно)
print("\n2. Фильтр по рейтингу (rating__gte=4.7):")
high_rated = Service.objects.filter(rating__gte=4.7)
print(f"   Услуги с рейтингом >= 4.7: {high_rated.count()}")
for s in high_rated:
    print(f"   - {s.title}: {s.rating}")

# 3. Фильтр по рейтингу (меньше)
print("\n3. Фильтр по рейтингу (rating__lt=4.0):")
low_rated = Service.objects.filter(rating__lt=4.0)
print(f"   Услуги с рейтингом < 4.0: {low_rated.count()}")
for s in low_rated:
    print(f"   - {s.title}: {s.rating}")

# 4. Фильтр по статусу (только опубликованные)
print("\n4. Фильтр по статусу (is_published=1):")
published = Service.objects.filter(is_published=Status.PUBLISHED)
print(f"   Опубликованные услуги: {published.count()}")
for s in published:
    print(f"   - {s.title}")

# 5. Фильтр по статусу (только черновики)
print("\n5. Фильтр по статусу (is_published=0):")
drafts = Service.objects.filter(is_published=Status.DRAFT)
print(f"   Черновики: {drafts.count()}")
for s in drafts:
    print(f"   - {s.title}")

# 6. Сложный фильтр (категория + рейтинг)
print("\n6. Сложный фильтр (СТО с рейтингом >= 4.5):")
good_sto = Service.objects.filter(
    category=cat_sto,
    rating__gte=4.5
)
print(f"   Найдено: {good_sto.count()}")
for s in good_sto:
    print(f"   - {s.title}: {s.rating}")

# 7. Поиск по тексту (icontains)
print("\n7. Поиск по тексту (title__icontains='эвакуатор'):")
search = Service.objects.filter(title__icontains='эвакуатор')
print(f"   Найдено: {search.count()}")
for s in search:
    print(f"   - {s.title}")

# 8. Исключение (exclude)
print("\n8. Исключение (exclude - все кроме черновиков):")
no_drafts = Service.objects.exclude(is_published=Status.DRAFT)
print(f"   Все кроме черновиков: {no_drafts.count()}")

print("\n" + "=" * 60)
print("ФИЛЬТРАЦИЯ ЗАВЕРШЕНА")
print("=" * 60)