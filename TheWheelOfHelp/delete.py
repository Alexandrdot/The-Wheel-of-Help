# step6_delete.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheWheelOfHelp.settings')
django.setup()

from homepage.models import Service, Category, Status

print("=" * 60)
print("ЭТАП 6: УДАЛЕНИЕ ЗАПИСЕЙ (DELETE)")
print("=" * 60)

# Показываем сколько записей до удаления
print(f"\nДО УДАЛЕНИЯ:")
print(f"Всего услуг в БД: {Service.objects.count()}")

# 1. Удаление одной записи
print("\n1. Удаление одной записи:")
print("-" * 40)

# Находим запись для удаления (например, черновик)
service_to_delete = Service.objects.filter(title__icontains='черновик').first()

if service_to_delete:
    print(f"Удаляем: {service_to_delete.title} (ID: {service_to_delete.id})")
    service_to_delete.delete()
    print(f"✅ Запись удалена")
else:
    print("Записей для удаления не найдено")

# Проверяем, что запись действительно удалена
try:
    deleted_check = Service.objects.get(title__icontains='черновик')
    print("❌ Ошибка: запись не удалена!")
except Service.DoesNotExist:
    print("✅ Проверка: запись действительно удалена из БД")

# 2. Массовое удаление
print("\n2. Массовое удаление (по условию):")
print("-" * 40)

# Создадим тестовые записи для массового удаления
print("Создаем тестовые записи для массового удаления...")

cat_sto = Category.objects.get(slug='tech-station')

# Создаем несколько тестовых услуг
test_services = []
for i in range(1, 4):
    service, created = Service.objects.get_or_create(
        slug=f'test-delete-{i}',
        defaults={
            'title': f'Тестовая услуга {i} (для удаления)',
            'description': 'Эта услуга будет удалена',
            'category': cat_sto,
            'address': 'ул. Тестовая, 1',
            'phone': '+7 (999) 000-00-00',
            'rating': 2.0,
            'is_published': Status.DRAFT
        }
    )
    if created:
        print(f'   ✅ Создана: "{service.title}"')
        test_services.append(service)
    else:
        print(f'   ⚠️ Уже существует: "{service.title}"')

# Показываем сколько записей перед массовым удалением
count_before = Service.objects.count()
print(f"\nЗаписей в БД перед массовым удалением: {count_before}")

# Массовое удаление всех тестовых записей
print("\nВыполняем массовое удаление записей, содержащих 'Тестовая' в названии...")
deleted_count = Service.objects.filter(title__icontains='Тестовая').delete()
print(f"✅ Удалено записей: {deleted_count[0]}")

# Проверяем результат
count_after = Service.objects.count()
print(f"\nЗаписей в БД после удаления: {count_after}")
print(f"Удалено всего: {count_before - count_after}")

# 3. Удаление по рейтингу (низкий рейтинг)
print("\n3. Удаление записей с низким рейтингом:")
print("-" * 40)

low_rated = Service.objects.filter(rating__lt=3.0)
low_count = low_rated.count()
print(f"Найдено записей с рейтингом < 3.0: {low_count}")

if low_count > 0:
    print("Удаляем их...")
    low_rated.delete()
    print(f"✅ Удалено {low_count} записей")
else:
    print("Нет записей с рейтингом < 3.0")

# 4. Финальная проверка
print("\n" + "=" * 60)
print("ИТОГОВАЯ ПРОВЕРКА")
print("=" * 60)

print(f"Всего услуг в БД: {Service.objects.count()}")

print("\nОставшиеся услуги:")
for s in Service.objects.all():
    status = "Опубликовано" if s.is_published else "Черновик"
    print(f"  - {s.title} (рейтинг: {s.rating}, {status})")

print("\n" + "=" * 60)
print("УДАЛЕНИЕ ЗАВЕРШЕНО")
print("=" * 60)