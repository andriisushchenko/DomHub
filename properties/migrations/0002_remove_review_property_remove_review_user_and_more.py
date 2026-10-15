
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='property',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AlterField(
            model_name='property',
            name='deal_type',
            field=models.CharField(choices=[('sale', 'Продаж'), ('rent', 'Аренда')], max_length=10),
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
