# step5_update.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheWheelOfHelp.settings')
django.setup()

from homepage.models import Service, Status

print("=" * 60)
print("ЭТАП 5: ИЗМЕНЕНИЕ ЗАПИСЕЙ (UPDATE)")
print("=" * 60)

# 1. Изменение одной записи
print("\n1. Изменение одной записи:")
print("-" * 40)

# Находим запись для изменения
service = Service.objects.get(slug='shinomontazh-koleso')
print(f"ДО изменения:")
print(f"   Название: {service.title}")
print(f"   Рейтинг: {service.rating}")
print(f"   Время работы: {service.work_time}")

# Изменяем поля
service.rating = 4.8
service.work_time = '09:00-23:00'
service.save()

print(f"\nПОСЛЕ изменения:")
print(f"   Рейтинг: {service.rating} (был 4.5)")
print(f"   Время работы: {service.work_time} (было 09:00-21:00)")

# 2. Изменение статуса (черновик -> опубликовано)
print("\n2. Изменение статуса публикации:")
print("-" * 40)

draft = Service.objects.filter(is_published=Status.DRAFT).first()
if draft:
    print(f"ДО: {draft.title} - статус: {'Черновик' if draft.is_published == Status.DRAFT else 'Опубликовано'}")
    
    draft.is_published = Status.PUBLISHED
    draft.save()
    
    print(f"ПОСЛЕ: {draft.title} - статус: {'Черновик' if draft.is_published == Status.DRAFT else 'Опубликовано'}")
else:
    print("Черновиков не найдено")

# 3. Массовое обновление (update)
print("\n3. Массовое обновление (update):")
print("-" * 40)

from homepage.models import Category
cat_sto = Category.objects.get(slug='tech-station')

# Обновляем время работы для всех СТО
count = Service.objects.filter(category=cat_sto).update(
    work_time='09:00-22:00'
)
print(f"Обновлено {count} услуг в категории 'СТО'")
print("Новое время работы для всех СТО: 09:00-22:00")

# Проверяем результат
print("\n4. Проверка изменений:")
print("-" * 40)
updated_service = Service.objects.get(slug='avtoservis-profi')
print(f"{updated_service.title}:")
print(f"   Рейтинг: {updated_service.rating}")
print(f"   Время работы: {updated_service.work_time}")

print("\n" + "=" * 60)
print("ИЗМЕНЕНИЕ ЗАВЕРШЕНО")
print("=" * 60)