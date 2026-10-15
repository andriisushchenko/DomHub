from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('Slug (для адреси)', max_length=100, unique=True)
    description = models.TextField('Опис', blank=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField("Ім'я", max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    photo = models.ImageField('Фото', upload_to='agents/', blank=True, null=True)
    bio = models.TextField('Про агента', blank=True)
    agency = models.CharField('Агентство', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенти'

    def __str__(self):
        return self.name


DEAL_TYPE_CHOICES = (
    ('sale', 'Продаж'),
    ('rent', 'Оренда'),
)


class Property(models.Model):
    title = models.CharField('Назва', max_length=200)
    description = models.TextField('Опис', blank=True)
    price = models.DecimalField('Ціна ($)', max_digits=12, decimal_places=2)
    deal_type = models.CharField('Тип угоди', max_length=10, choices=DEAL_TYPE_CHOICES)
    area_sqm = models.FloatField('Площа (м²)')
    rooms = models.PositiveIntegerField('Кількість кімнат')
    address = models.CharField('Адреса', max_length=255)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField('Довгота', max_digits=9, decimal_places=6, blank=True, null=True)
    main_image = models.ImageField('Головне фото', upload_to='properties/')
    is_active = models.BooleanField('Активне оголошення', default=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name='Власник')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True, related_name='properties', verbose_name='Агент')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='properties', verbose_name='Категорія')

    class Meta:
        verbose_name = "Об'єкт"
        verbose_name_plural = "Об'єкти"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('property_detail', args=[self.pk])


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name="Об'єкт")
    image = models.ImageField('Фото', upload_to='properties/gallery/')
    caption = models.CharField('Підпис', max_length=200, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фото галереї'
        verbose_name_plural = 'Фото галереї'

    def __str__(self):
        return f'Фото для {self.property.title}'
