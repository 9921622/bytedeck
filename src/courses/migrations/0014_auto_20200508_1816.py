# Generated by Django 2.2.12 on 2020-05-09 01:16

from django.db import migrations


# Can't use fixtures because load_fixtures method is janky with django-tenant-schemas
def load_initial_data(apps, schema_editor):
    Block = apps.get_model('courses', 'Block')

    # add some initial data if none has been created yet
    if not Block.objects.exists():
        Block.objects.create(
            block="Default Block",
        )


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20200425_2052'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
