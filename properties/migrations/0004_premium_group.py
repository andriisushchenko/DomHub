from django.db import migrations


def create_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Premium')


def delete_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Premium').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('properties', '0003_alter_agent_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_group, delete_group),
    ]
