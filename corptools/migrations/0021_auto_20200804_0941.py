# Generated by Django 2.2.12 on 2020-08-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corptools', '0020_clone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jumpclone',
            name='location_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='jumpclone',
            name='location_type',
            field=models.CharField(choices=[('station', 'station'), ('structure', 'structure')], default=None, max_length=9, null=True),
        ),
    ]
