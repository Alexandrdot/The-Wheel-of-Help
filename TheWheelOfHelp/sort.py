# step4_order.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheWheelOfHelp.settings')
django.setup()

from homepage.models import Service

print("=" * 60)
print("ЭТАП 4: СОРТИРОВКА ЗАПИСЕЙ (ORDER BY)")
print("=" * 60)

# 1. Сортировка по рейтингу (убывание - от высокого к низкому)
print("\n1. Сортировка по рейтингу (убывание):")
print("-" * 40)
sorted_by_rating_desc = Service.objects.all().order_by('-rating')
for i, s in enumerate(sorted_by_rating_desc, 1):
    print(f"{i:2}. {s.rating} - {s.title}")

# 2. Сортировка по рейтингу (возрастание - от низкого к высокому)
print("\n2. Сортировка по рейтингу (возрастание):")
print("-" * 40)
sorted_by_rating_asc = Service.objects.all().order_by('rating')
for i, s in enumerate(sorted_by_rating_asc, 1):
    print(f"{i:2}. {s.rating} - {s.title}")

# 3. Сортировка по названию (алфавит)
print("\n3. Сортировка по названию (А-Я):")
print("-" * 40)
sorted_by_title = Service.objects.all().order_by('title')
for i, s in enumerate(sorted_by_title, 1):
    print(f"{i:2}. {s.title}")

# 4. Сортировка по дате создания (новые сверху)
print("\n4. Сортировка по дате создания (новые сверху):")
print("-" * 40)
sorted_by_date = Service.objects.all().order_by('-time_create')
for i, s in enumerate(sorted_by_date[:5], 1):  # только первые 5
    date_str = s.time_create.strftime('%d.%m.%Y %H:%M')
    print(f"{i:2}. {date_str} - {s.title}")

# 5. Комбинирование: фильтр + сортировка
print("\n5. Комбинирование: фильтр + сортировка")
print("   (СТО с рейтингом >= 4.5, отсортированы по убыванию рейтинга):")
print("-" * 40)
from homepage.models import Category
cat_sto = Category.objects.get(slug='tech-station')
filtered_sorted = Service.objects.filter(
    category=cat_sto,
    rating__gte=4.5
).order_by('-rating')
for i, s in enumerate(filtered_sorted, 1):
    print(f"{i:2}. {s.rating} - {s.title}")

print("\n" + "=" * 60)
print("СОРТИРОВКА ЗАВЕРШЕНА")
print("=" * 60)