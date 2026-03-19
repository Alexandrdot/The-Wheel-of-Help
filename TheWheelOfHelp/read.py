# step2_read.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheWheelOfHelp.settings')
django.setup()

from homepage.models import Category, Service

print("=" * 60)
print("ЭТАП 2: ЧТЕНИЕ ЗАПИСЕЙ (READ)")
print("=" * 60)

# 1. Чтение всех записей
print("\n1. Чтение всех записей (all()):")
all_services = Service.objects.all()
print(f"   Всего услуг в БД: {all_services.count()}")

# 2. Чтение первой записи
print("\n2. Чтение первой записи (first()):")
first = Service.objects.first()
print(f"   Первая услуга: {first.title} (ID: {first.id})")

# 3. Чтение записи по ID
print("\n3. Чтение записи по ID (get(id=...)):")
try:
    service = Service.objects.get(id=1)
    print(f"   Услуга с ID=1: {service.title}")
except Service.DoesNotExist:
    print("   Услуга с ID=1 не найдена")

# 4. Чтение записи по слагу
print("\n4. Чтение записи по слагу (get(slug=...)):")
try:
    service = Service.objects.get(slug='evakuator-247')
    print(f"   Услуга со слагом 'evakuator-247': {service.title}")
except Service.DoesNotExist:
    print("   Услуга не найдена")

# 5. Вывод всех записей в табличном виде
print("\n5. Все записи в БД:")
print("-" * 60)
print(f"{'ID':<4} {'Название':<25} {'Рейтинг':<8} {'Статус':<12} Категория")
print("-" * 60)

for service in Service.objects.all():
    status = "Опубликовано" if service.is_published else "Черновик"
    print(f"{service.id:<4} {service.title[:25]:<25} {service.rating:<8} {status:<12} {service.category.name}")
print("-" * 60)

print("\n" + "=" * 60)
print("ЧТЕНИЕ ЗАВЕРШЕНО")
print("=" * 60)