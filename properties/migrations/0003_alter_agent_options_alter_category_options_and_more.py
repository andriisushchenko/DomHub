
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_remove_review_property_remove_review_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agent',
            options={'verbose_name': 'Агент', 'verbose_name_plural': 'Агенти'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категорія', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name': "Об'єкт", 'verbose_name_plural': "Об'єкти"},
        ),
        migrations.AlterModelOptions(
            name='propertyimage',
            options={'verbose_name': 'Фото галереї', 'verbose_name_plural': 'Фото галереї'},
        ),
        migrations.AlterField(
            model_name='agent',
            name='agency',
            field=models.CharField(blank=True, max_length=100, verbose_name='Агентство'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Про агента'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='name',
            field=models.CharField(max_length=100, verbose_name="Ім'я"),
        ),
        migrations.AlterField(
            model_name='agent',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='agents/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Назва'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug (для адреси)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адреса'),
        ),
        migrations.AlterField(
            model_name='property',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='properties', to='properties.agent', verbose_name='Агент'),
        ),
        migrations.AlterField(
            model_name='property',
            name='area_sqm',
            field=models.FloatField(verbose_name='Площа (м²)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='properties', to='properties.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='property',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Створено'),
        ),
        migrations.AlterField(
            model_name='property',
            name='deal_type',
            field=models.CharField(choices=[('sale', 'Продаж'), ('rent', 'Оренда')], max_length=10, verbose_name='Тип угоди'),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис'),
        ),
        migrations.AlterField(
            model_name='property',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активне оголошення'),
        ),
        migrations.AlterField(
            model_name='property',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='property',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Довгота'),
        ),
        migrations.AlterField(
            model_name='property',
            name='main_image',
            field=models.ImageField(upload_to='properties/', verbose_name='Головне фото'),
        ),
        migrations.AlterField(
            model_name='property',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL, verbose_name='Власник'),
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Ціна ($)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='rooms',
            field=models.PositiveIntegerField(verbose_name='Кількість кімнат'),
        ),
        migrations.AlterField(
            model_name='property',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Назва'),
        ),
        migrations.AlterField(
            model_name='property',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Оновлено'),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='caption',
            field=models.CharField(blank=True, max_length=200, verbose_name='Підпис'),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='image',
            field=models.ImageField(upload_to='properties/gallery/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='properties.property', verbose_name="Об'єкт"),
        ),
    ]
