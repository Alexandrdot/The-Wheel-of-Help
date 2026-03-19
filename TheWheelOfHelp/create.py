from homepage.models import Category, Service, Status

print("=" * 60)
print("ЭТАП 1: СОЗДАНИЕ ЗАПИСЕЙ (CREATE)")
print("=" * 60)

# Получаем существующие категории
print("\n1. Получаем категории из БД:")
categories = Category.objects.all()
for cat in categories:
    print(f"   - {cat.name} (slug: {cat.slug})")

# Создаем новые услуги
print("\n2. Создаем новые услуги:")

# Создаем СТО
cat_sto = Category.objects.get(slug='tech-station')
service1 = Service.objects.create(
    title='Автосервис "Профи"',
    slug='avtoservis-profi',
    description='Профессиональный ремонт двигателей, ходовой части, диагностика',
    category=cat_sto,
    address='ул. Ленина, 10',
    phone='+7 (999) 111-22-33',
    work_time='09:00-21:00',
    rating=4.7,
    is_published=Status.PUBLISHED
)
print(f'   ✅ Создана: "{service1.title}" (ID: {service1.id})')

# Создаем Эвакуатор
cat_evac = Category.objects.get(slug='evacuators')
service2 = Service.objects.create(
    title='Эвакуатор 24/7',
    slug='evakuator-247',
    description='Круглосуточная эвакуация легковых и грузовых автомобилей',
    category=cat_evac,
    address='ул. Московская, 5',
    phone='+7 (999) 222-33-44',
    work_time='круглосуточно',
    rating=4.9,
    is_published=Status.PUBLISHED
)
print(f'   ✅ Создана: "{service2.title}" (ID: {service2.id})')

# Создаем Шиномонтаж
cat_tire = Category.objects.get(slug='tire-services')
service3 = Service.objects.create(
    title='Шиномонтаж "Колесо"',
    slug='shinomontazh-koleso',
    description='Сезонная замена шин, балансировка, правка дисков',
    category=cat_tire,
    address='пр. Мира, 42',
    phone='+7 (999) 333-44-55',
    work_time='09:00-21:00',
    rating=4.5,
    is_published=Status.PUBLISHED
)
print(f'   ✅ Создана: "{service3.title}" (ID: {service3.id})')

# Создаем черновик (для теста фильтрации)
service_draft = Service.objects.create(
    title='Тестовая услуга (черновик)',
    slug='test-draft',
    description='Это черновик, не должен отображаться на сайте',
    category=cat_sto,
    address='ул. Тестовая, 1',
    phone='+7 (999) 000-00-00',
    rating=3.0,
    is_published=Status.DRAFT  # 0 - черновик
)
print(f'   ✅ Создана: "{service_draft.title}" (ID: {service_draft.id}) - ЧЕРНОВИК')

print("\n" + "=" * 60)
print(f"ИТОГ: Создано {Service.objects.count()} услуг")
print("=" * 60)