from django.core.management.base import BaseCommand
from django.db import transaction

from homepage.constants import CATEGORY_SLUG_STO, CATEGORY_SLUG_TIRE, CATEGORY_SLUG_TOW
from homepage.models import CarService, Category, Status, Tag, TireService, TowTruck

CATEGORIES = [
    (CATEGORY_SLUG_STO, 'СТО'),
    (CATEGORY_SLUG_TIRE, 'Шиномонтаж'),
    (CATEGORY_SLUG_TOW, 'Эвакуаторы'),
]

TAGS = [
    ('kruglosutochno', 'Круглосуточно'),
    ('garantiya', 'Гарантия'),
    ('opytnye-mastera', 'Опытные мастера'),
    ('besplatnaya-diagnostika', 'Бесплатная диагностика'),
]

CAR_SERVICES = [
    ('avto-master-1', 'АвтоМастер на Ленина', 'Ремонт двигателей и ходовой', 'ул. Ленина, 12', '89001234501', '08:00–20:00', 4.6, 'Двигатели, ходовая', True),
    ('sto-vostok', 'СТО Восток', 'Комплексное обслуживание легковых авто', 'пр. Мира, 45', '89001234502', '09:00–21:00', 4.8, 'ТО, диагностика', True),
    ('garazh-24', 'Гараж 24', 'Срочный ремонт и эвакуация партнёров', 'ул. Гагарина, 7', '89001234503', 'круглосуточно', 4.2, 'Срочный ремонт', True),
    ('motor-servis', 'МоторСервис', 'Капитальный и текущий ремонт', 'ул. Советская, 88', '89001234504', '10:00–19:00', 4.5, 'Капремонт', True),
    ('avto-lider', 'АвтоЛидер', 'Слесарные работы любой сложности', 'ул. Победы, 3', '89001234505', '08:30–20:30', 4.7, 'Слесарка', True),
    ('pro-sto', 'ПроСТО', 'Диагностика и ремонт иномарок', 'ул. Заводская, 19', '89001234506', '09:00–18:00', 4.9, 'Иномарки', True),
    ('remont-plus', 'Ремонт Плюс', 'Кузовной ремонт и покраска', 'ул. Садовая, 55', '89001234507', '10:00–20:00', 4.3, 'Кузов, покраска', False),
    ('avtohaus', 'АвтоХаус', 'Техобслуживание и замена масла', 'ул. Центральная, 21', '89001234508', '08:00–22:00', 4.4, 'ТО, масло', True),
    ('master-auto', 'МастерАвто', 'Ремонт АКПП и подвески', 'ул. Южная, 9', '89001234509', '09:00–19:30', 4.6, 'АКПП, подвеска', True),
    ('sto-sever', 'СТО Север', 'Предпродажная подготовка', 'ул. Северная, 33', '89001234510', '10:00–18:00', 4.1, 'Предпродажка', True),
    ('drive-service', 'Drive Service', 'Компьютерная диагностика всех марок', 'ул. Автомобилистов, 2', '89001234511', '08:00–20:00', 4.8, 'Диагностика', True),
    ('technik-sto', 'Техник СТО', 'Замена ГРМ и тормозов', 'ул. Промышленная, 14', '89001234512', '09:00–20:00', 4.5, 'ГРМ, тормоза', True),
]

TIRE_SERVICES = [
    ('shina-pro-1', 'ШинаПро Центр', 'Шиномонтаж и балансировка', 'ул. Ленина, 50', '89002234501', '08:00–22:00', 4.5, 14, 22, True),
    ('koleso-24', 'Колесо 24', 'Сезонная замена и хранение шин', 'пр. Победы, 11', '89002234502', 'круглосуточно', 4.7, 13, 21, True),
    ('shinomontazh-vostok', 'Шиномонтаж Восток', 'Ремонт проколов и грыж', 'ул. Восточная, 6', '89002234503', '09:00–21:00', 4.3, 15, 20, False),
    ('r13-r22', 'R13–R22 Сервис', 'Легковые и кроссоверы', 'ул. Молодёжная, 18', '89002234504', '10:00–20:00', 4.6, 13, 22, True),
    ('shina-lider', 'ШинаЛидер', 'Быстрый монтаж без записи', 'ул. Гаражная, 4', '89002234505', '08:30–21:30', 4.4, 14, 21, False),
    ('pro-koleso', 'ПроКолесо', 'Продажа и установка шин', 'ул. Торговая, 27', '89002234506', '09:00–19:00', 4.8, 15, 22, True),
    ('shina-master', 'ШинаМастер', 'Балансировка и развал-схождение', 'ул. Зелёная, 9', '89002234507', '10:00–18:00', 4.2, 14, 20, False),
    ('koleso-plus', 'Колесо Плюс', 'Хранение шин на складе', 'ул. Складская, 1', '89002234508', '08:00–20:00', 4.5, 13, 21, True),
    ('shina-ekspress', 'ШинаЭкспресс', 'Монтаж за 20 минут', 'ул. Быстрая, 15', '89002234509', '09:00–22:00', 4.9, 14, 22, False),
    ('zimnie-shiny', 'ЗимниеШины', 'Сезонный шиномонтаж', 'ул. Снежная, 8', '89002234510', '10:00–19:00', 4.1, 13, 20, True),
    ('shina-sever', 'ШинаСевер', 'Грузовой и легковой монтаж', 'ул. Северная, 44', '89002234511', '08:00–21:00', 4.6, 16, 22, True),
    ('koleso-garant', 'КолесоГарант', 'Гарантия на все работы', 'ул. Гарантийная, 3', '89002234512', '09:00–20:00', 4.7, 14, 21, True),
]

TOW_TRUCKS = [
    ('evakuator-1', 'Эвакуатор Экспресс', 'Быстрая подача по городу', 'ул. Транспортная, 1', '89003234501', 'круглосуточно', 4.6, 3, True),
    ('evak-24', 'Эвак 24', 'Легковые и кроссоверы', 'ул. Ночная, 5', '89003234502', 'круглосуточно', 4.8, 2, True),
    ('gruz-evak', 'ГрузЭвак', 'Эвакуация до 5 тонн', 'пр. Грузовой, 12', '89003234503', 'круглосуточно', 4.4, 5, True),
    ('evakuator-plus', 'Эвакуатор Плюс', 'Подача за 30 минут', 'ул. Быстрая, 20', '89003234504', '00:00–24:00', 4.5, 2, True),
    ('doroga-pomosh', 'ДорогаПомощь', 'Техпомощь на трассе', 'ул. Трасса, 100', '89003234505', 'круглосуточно', 4.3, 4, True),
    ('evak-lider', 'ЭвакЛидер', 'Бережная погрузка', 'ул. Бережная, 7', '89003234506', 'круглосуточно', 4.7, 3, True),
    ('mega-evak', 'МегаЭвак', 'Крупногабаритный транспорт', 'ул. Промышленная, 50', '89003234507', '08:00–22:00', 4.2, 8, False),
    ('evak-moskva', 'ЭвакМосква', 'Работа по области', 'ул. Областная, 2', '89003234508', 'круглосуточно', 4.6, 3, True),
    ('sluzhba-evak', 'СлужбаЭвак', 'Фиксированные тарифы', 'ул. Тарифная, 9', '89003234509', 'круглосуточно', 4.5, 2, True),
    ('evak-garant', 'ЭвакГарант', 'Страховые случаи', 'ул. Страховая, 14', '89003234510', '09:00–21:00', 4.1, 2, False),
    ('noch-evak', 'НочьЭвак', 'Ночная эвакуация', 'ул. Лунная, 6', '89003234511', '20:00–08:00', 4.4, 2, True),
    ('evak-pro', 'ЭвакПро', 'Профессиональная эвакуация', 'ул. Профессиональная, 11', '89003234512', 'круглосуточно', 4.9, 4, True),
]


class Command(BaseCommand):
    help = 'Заполняет категории, теги и по 12 услуг каждого типа (СТО, шиномонтаж, эвакуаторы).'

    @transaction.atomic
    def handle(self, *args, **options):
        cats = {}
        for slug, name in CATEGORIES:
            cat, created = Category.objects.update_or_create(slug=slug, defaults={'name': name})
            cats[slug] = cat
            self.stdout.write(f"{'Создана' if created else 'Обновлена'} категория: {name}")

        tags = {}
        for slug, name in TAGS:
            tag, _ = Tag.objects.update_or_create(slug=slug, defaults={'name': name})
            tags[slug] = tag

        car_count = self._seed_cars(cats[CATEGORY_SLUG_STO], tags)
        tire_count = self._seed_tires(cats[CATEGORY_SLUG_TIRE], tags)
        tow_count = self._seed_tows(cats[CATEGORY_SLUG_TOW], tags)

        self.stdout.write(self.style.SUCCESS(
            f'Готово: СТО — {car_count}, шиномонтаж — {tire_count}, эвакуаторы — {tow_count}'
        ))

    def _seed_cars(self, category, tags):
        count = 0
        for slug, title, desc, address, phone, work_time, rating, spec, diag in CAR_SERVICES:
            obj, created = CarService.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'address': address,
                    'phone': phone,
                    'work_time': work_time,
                    'rating': rating,
                    'is_published': Status.PUBLISHED,
                    'category': category,
                    'specialization': spec,
                    'diagnostic_available': diag,
                },
            )
            if created:
                obj.tags.set([tags['garantiya'], tags['opytnye-mastera']])
            count += 1
        return count

    def _seed_tires(self, category, tags):
        count = 0
        for slug, title, desc, address, phone, work_time, rating, r_from, r_to, storage in TIRE_SERVICES:
            obj, created = TireService.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'address': address,
                    'phone': phone,
                    'work_time': work_time,
                    'rating': rating,
                    'is_published': Status.PUBLISHED,
                    'category': category,
                    'wheel_size_from': r_from,
                    'wheel_size_to': r_to,
                    'tire_storage': storage,
                },
            )
            if created:
                obj.tags.set([tags['kruglosutochno'], tags['garantiya']])
            count += 1
        return count

    def _seed_tows(self, category, tags):
        count = 0
        for slug, title, desc, address, phone, work_time, rating, capacity, work_24_7 in TOW_TRUCKS:
            obj, created = TowTruck.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'address': address,
                    'phone': phone,
                    'work_time': work_time,
                    'rating': rating,
                    'is_published': Status.PUBLISHED,
                    'category': category,
                    'load_capacity': capacity,
                    'work_24_7': work_24_7,
                },
            )
            if created:
                obj.tags.set([tags['kruglosutochno'], tags['besplatnaya-diagnostika']])
            count += 1
        return count
