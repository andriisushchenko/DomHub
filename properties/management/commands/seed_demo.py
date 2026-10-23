import io
import random
import urllib.request

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from PIL import Image, ImageDraw

from properties.models import Agent, Category, Property, PropertyImage

CATEGORIES = [
    ('kvartira', 'Квартира'),
    ('budynok', 'Будинок'),
    ('penthouse', 'Пентхаус'),
    ('office', 'Офіс'),
]

AGENTS = [
    ('Олена Коваль', 'olena@domhub.ua', '+380671234501', 'DomHub Київ'),
    ('Андрій Мельник', 'andrii@domhub.ua', '+380671234502', 'DomHub Київ'),
    ('Ірина Бондар', 'iryna@domhub.ua', '+380671234503', 'Львів Нерухомість'),
    ('Максим Шевчук', 'maksym@domhub.ua', '+380671234504', 'Південь Ріелт'),
]

PROPERTIES = [
    ('Світла квартира біля Арсенальної', 'kvartira', 'sale', 'Київ, Печерськ, вул. Івана Мазепи, 10', 50.4440, 30.5450, 2, 64),
    ('Квартира з видом на Дніпро', 'kvartira', 'sale', 'Київ, Оболонь, Оболонська набережна, 7', 50.5040, 30.5180, 3, 92),
    ('Студія біля метро Лук\'янівська', 'kvartira', 'rent', 'Київ, Шевченківський р-н, вул. Мельникова, 2', 50.4620, 30.4820, 1, 32),
    ('Двокімнатна на Подолі', 'kvartira', 'rent', 'Київ, Поділ, вул. Сагайдачного, 25', 50.4650, 30.5170, 2, 58),
    ('Сучасна квартира в ЖК на Позняках', 'kvartira', 'sale', 'Київ, Дарницький р-н, вул. Драгоманова, 31', 50.3980, 30.6300, 2, 70),
    ('Пентхаус з терасою в центрі', 'penthouse', 'sale', 'Київ, Шевченківський р-н, вул. Хрещатик, 15', 50.4470, 30.5220, 4, 210),
    ('Пентхаус на Печерських пагорбах', 'penthouse', 'rent', 'Київ, Печерськ, вул. Липська, 4', 50.4430, 30.5340, 3, 160),
    ('Будинок у Конча-Заспі', 'budynok', 'sale', 'Київ, Голосіївський р-н, Конча-Заспа', 50.3020, 30.5890, 5, 320),
    ('Котедж на Осокорках', 'budynok', 'rent', 'Київ, Дарницький р-н, Осокорки', 50.3920, 30.6150, 4, 180),
    ('Офіс класу A на Лівому березі', 'office', 'rent', 'Київ, Дніпровський р-н, Русанівська набережна, 12', 50.4370, 30.5970, 0, 140),
    ('Офіс біля Контрактової площі', 'office', 'sale', 'Київ, Поділ, Контрактова площа, 4', 50.4650, 30.5150, 0, 85),
    ('Квартира в австрійському будинку', 'kvartira', 'sale', 'Львів, Галицький р-н, вул. Городоцька, 18', 49.8380, 24.0170, 3, 86),
    ('Затишна квартира біля Ратуші', 'kvartira', 'rent', 'Львів, площа Ринок, 9', 49.8420, 24.0320, 2, 55),
    ('Будинок у Брюховичах', 'budynok', 'sale', 'Львів, Брюховичі, вул. Лісова, 3', 49.9050, 23.9700, 4, 210),
    ('Пентхаус з видом на Високий замок', 'penthouse', 'sale', 'Львів, вул. Замкова, 6', 49.8480, 24.0390, 3, 140),
    ('Квартира біля моря в Аркадії', 'kvartira', 'sale', 'Одеса, Аркадія, Генуезька вул., 5', 46.4290, 30.7600, 2, 68),
    ('Студія на Дерибасівській', 'kvartira', 'rent', 'Одеса, вул. Дерибасівська, 12', 46.4840, 30.7380, 1, 30),
    ('Будинок на Фонтані', 'budynok', 'sale', 'Одеса, Великий Фонтан, 13 ст.', 46.3830, 30.7420, 5, 260),
    ('Офіс у бізнес-центрі', 'office', 'rent', 'Одеса, вул. Французький бульвар, 22', 46.4650, 30.7550, 0, 110),
    ('Квартира в центрі Дніпра', 'kvartira', 'sale', 'Дніпро, просп. Дмитра Яворницького, 50', 48.4680, 35.0420, 3, 79),
    ('Квартира біля набережної', 'kvartira', 'rent', 'Дніпро, Січеславська набережна, 15', 48.4600, 35.0700, 2, 60),
    ('Пентхаус над Дніпром', 'penthouse', 'sale', 'Дніпро, вул. Набережна Перемоги, 32', 48.4340, 35.0600, 4, 190),
    ('Квартира біля парку Горького', 'kvartira', 'sale', 'Харків, вул. Сумська, 81', 50.0140, 36.2280, 2, 62),
    ('Будинок на Салтівці', 'budynok', 'rent', 'Харків, Салтівка, вул. Гвардійців-Широнінців, 3', 50.0300, 36.3400, 3, 120),
]

PRICES = {
    ('kvartira', 'sale'): (45_000, 250_000),
    ('kvartira', 'rent'): (350, 1_500),
    ('penthouse', 'sale'): (250_000, 900_000),
    ('penthouse', 'rent'): (2_000, 6_000),
    ('budynok', 'sale'): (120_000, 700_000),
    ('budynok', 'rent'): (1_000, 4_000),
    ('office', 'sale'): (90_000, 400_000),
    ('office', 'rent'): (800, 5_000),
}

DESCRIPTIONS = [
    'Простора та світла {kind} площею {area} м². Якісний ремонт, нові вікна та сантехніка.',
    'Поруч розвинена інфраструктура: магазини, школи, парки та зупинки громадського транспорту.',
    'Тихий двір, охорона та паркінг. Документи готові, можливий швидкий вихід на угоду.',
    'Чудовий варіант як для життя, так і для інвестицій. Перегляд у зручний для вас час.',
]

EXTERIOR_PHOTOS = {
    'kvartira': ['1545324418-cc1a3fa10c00', '1460317442991-0ec209397118', '1515263487990-61b07816b324',
                 '1574362848149-11496d93a7c7', '1567496898669-ee935f5f647a'],
    'penthouse': ['1512917774080-9991f1c4c750', '1600596542815-ffad4c1539a9', '1613490493576-7fde63acd811',
                  '1599809275671-b5942cabc7a2'],
    'budynok': ['1449844908441-8829872d2607', '1494526585095-c41746248156', '1558036117-15d82a90b9b1',
                '1564013799919-ab600027ffc6', '1568605114967-8130f3a36994', '1570129477492-45c003edd2be',
                '1576941089067-2de3c901e126', '1580587771525-78b9dba3b914', '1600047509358-9dc75507daeb',
                '1600047509807-ba8f99d2cdde', '1600566753190-17f0baa2a6c3', '1600585154340-be6161a56a0c',
                '1605276374104-dee2a0ed3cd6', '1416331108676-a22ccb276e35'],
    'office': ['1486406146926-c627a92ad1ab', '1600585154526-990dced4db0d', '1497366216548-37526070297c'],
}

INTERIOR_PHOTOS = {
    'kvartira': ['1484154218962-a197022b5858', '1493809842364-78817add7ffb', '1502672260266-1c1ef2d93688',
                 '1505691938895-1758d7feb511', '1522708323590-d24dbb6b0267', '1529408686214-b48b8532f72c',
                 '1554995207-c18c203602cb', '1556912173-3bb406ef7e77', '1600210492486-724fe5c67fb0',
                 '1616594039964-ae9021a400a0'],
    'penthouse': ['1560448204-e02f11c3d0e2', '1598928506311-c55ded91a20c', '1600573472550-8090b5e0745e',
                  '1600607687939-ce8a6c25118c', '1616594039964-ae9021a400a0'],
    'budynok': ['1484154218962-a197022b5858', '1493809842364-78817add7ffb', '1505691938895-1758d7feb511',
                '1522708323590-d24dbb6b0267', '1556912173-3bb406ef7e77', '1598928506311-c55ded91a20c',
                '1600210492486-724fe5c67fb0', '1600607687939-ce8a6c25118c'],
    'office': ['1497366216548-37526070297c', '1497366811353-6870744d04b2'],
}

KIND_NAMES = {'kvartira': 'квартира', 'penthouse': 'пентхаус', 'budynok': 'будинок', 'office': 'офіс'}

PALETTES = [
    ((135, 186, 230), (226, 232, 240), (99, 102, 241)),
    ((250, 204, 160), (241, 245, 249), (15, 23, 42)),
    ((167, 214, 196), (254, 243, 199), (180, 83, 9)),
    ((196, 181, 253), (248, 250, 252), (30, 64, 175)),
    ((253, 186, 116), (255, 255, 255), (127, 29, 29)),
]


def picture(seed, kind):
    rnd = random.Random(seed)
    sky, wall, roof = rnd.choice(PALETTES)
    img = Image.new('RGB', (900, 560), sky)
    draw = ImageDraw.Draw(img)
    for y in range(560):
        k = y / 560
        draw.line([(0, y), (900, y)], fill=tuple(int(c * (1 - 0.25 * k)) for c in sky))
    draw.rectangle([0, 430, 900, 560], fill=(120, 170, 110))

    if kind in ('kvartira', 'penthouse', 'office'):
        floors = rnd.randint(5, 9)
        x0, x1 = rnd.randint(220, 300), rnd.randint(600, 680)
        top = 430 - floors * 40
        draw.rectangle([x0, top, x1, 430], fill=wall, outline=(100, 116, 139), width=3)
        for f in range(floors):
            for wx in range(x0 + 25, x1 - 30, 55):
                y = top + 10 + f * 40
                draw.rectangle([wx, y, wx + 30, y + 22], fill=(56, 189, 248) if rnd.random() > 0.3 else (253, 224, 71))
        if kind == 'penthouse':
            draw.rectangle([x0 + 60, top - 50, x1 - 60, top], fill=roof)
            draw.rectangle([x0 + 90, top - 38, x1 - 90, top - 12], fill=(186, 230, 253))
    else:
        draw.rectangle([270, 270, 630, 430], fill=wall, outline=(100, 116, 139), width=3)
        draw.polygon([(240, 275), (450, 150), (660, 275)], fill=roof)
        draw.rectangle([420, 340, 480, 430], fill=(120, 72, 40))
        for wx in (310, 530):
            draw.rectangle([wx, 305, wx + 60, 360], fill=(56, 189, 248))
        for tx in (120, 760):
            draw.rectangle([tx + 18, 360, tx + 30, 430], fill=(120, 72, 40))
            draw.ellipse([tx - 20, 290, tx + 70, 380], fill=(74, 140, 80))

    buffer = io.BytesIO()
    img.save(buffer, 'JPEG', quality=85)
    return ContentFile(buffer.getvalue())


def download(photo_id):
    url = f'https://images.unsplash.com/photo-{photo_id}?w=1200&q=80&fit=crop'
    request = urllib.request.Request(url, headers={'User-Agent': 'DomHub seed_demo'})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.headers.get_content_type() != 'image/jpeg':
                return None
            return ContentFile(response.read())
    except OSError:
        return None


def photo(photo_id, fallback_seed, kind):
    return download(photo_id) or picture(fallback_seed, kind)


def avatar(seed):
    rnd = random.Random(seed)
    color = rnd.choice(PALETTES)[2]
    img = Image.new('RGB', (200, 200), color)
    draw = ImageDraw.Draw(img)
    draw.ellipse([60, 35, 140, 115], fill=(241, 245, 249))
    draw.ellipse([30, 125, 170, 260], fill=(241, 245, 249))
    buffer = io.BytesIO()
    img.save(buffer, 'JPEG', quality=85)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = 'Створює демо-категорії, агентів та об\'єкти нерухомості з фото.'

    def add_arguments(self, parser):
        parser.add_argument('--owners', help='Логіни власників через кому (за замовчуванням — усі користувачі).')
        parser.add_argument('--reset', action='store_true', help='Видалити демо-об\'єкти та створити заново.')

    def handle(self, *args, **options):
        if options['owners']:
            names = [n.strip() for n in options['owners'].split(',') if n.strip()]
            owners = list(User.objects.filter(username__in=names).order_by('id'))
            missing = set(names) - {u.username for u in owners}
            if missing:
                raise CommandError(f'Не знайдено користувачів: {", ".join(sorted(missing))}')
        else:
            owners = list(User.objects.order_by('id'))
        if not owners:
            raise CommandError('У базі немає користувачів. Створіть хоча б одного.')

        if options['reset']:
            titles = [p[0] for p in PROPERTIES]
            for prop in Property.objects.filter(title__in=titles):
                for img in prop.images.all():
                    img.image.delete(save=False)
                prop.main_image.delete(save=False)
                prop.delete()
            self.stdout.write('Старі демо-об\'єкти видалено.')

        categories = {}
        for slug, name in CATEGORIES:
            categories[slug], _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})

        agents = []
        for i, (name, email, phone, agency) in enumerate(AGENTS):
            agent, created = Agent.objects.get_or_create(
                email=email,
                defaults={'name': name, 'phone': phone, 'agency': agency,
                          'bio': 'Досвідчений агент з нерухомості.'},
            )
            if created:
                agent.photo.save(f'agent_{i}.jpg', avatar(i))
            agents.append(agent)

        rnd = random.Random(42)
        created_count = 0
        for i, (title, cat, deal, address, lat, lng, rooms, area) in enumerate(PROPERTIES):
            if Property.objects.filter(title=title).exists():
                continue
            low, high = PRICES[(cat, deal)]
            step = 10 if deal == 'rent' else 1000
            price = rnd.randint(low // step, high // step) * step
            description = '\n\n'.join(DESCRIPTIONS).format(kind=KIND_NAMES[cat], area=area)

            prop = Property(
                title=title,
                description=description,
                price=price,
                deal_type=deal,
                area_sqm=area,
                rooms=rooms,
                address=address,
                latitude=lat,
                longitude=lng,
                owner=owners[i % len(owners)],
                agent=agents[i % len(agents)] if i % 5 else None,
                category=categories[cat],
            )
            exteriors = EXTERIOR_PHOTOS[cat]
            interiors = INTERIOR_PHOTOS[cat]
            prop.main_image.save(f'demo_{i}.jpg', photo(exteriors[i % len(exteriors)], i, cat), save=False)
            prop.save()
            for g in range(2):
                gallery = PropertyImage(property=prop, order=g)
                interior = interiors[(i * 2 + g) % len(interiors)]
                gallery.image.save(f'demo_{i}_{g}.jpg', photo(interior, i * 10 + g + 1, cat), save=False)
                gallery.save()
            created_count += 1
            self.stdout.write(f'  {title} → {prop.owner.username}')

        self.stdout.write(self.style.SUCCESS(
            f'Готово: створено {created_count} об\'єктів (власники: {", ".join(u.username for u in owners)}).'
        ))
