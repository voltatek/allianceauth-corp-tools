# Generated by Django 3.2.5 on 2021-07-19 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corptools', '0051_auto_20210713_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationContactLabel',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('label_id', models.BigIntegerField()),
                ('label_name', models.CharField(max_length=255)),
                ('corporation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.corporationaudit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CorporationContact',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('contact_id', models.BigIntegerField()),
                ('contact_type', models.CharField(max_length=255)),
                ('standing', models.DecimalField(decimal_places=2, max_digits=4)),
                ('watched', models.BooleanField(default=False)),
                ('contact_name', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.evename')),
                ('corporation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.corporationaudit')),
                ('labels', models.ManyToManyField(
                    to='corptools.CorporationContactLabel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CharacterContactLabel',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('label_id', models.BigIntegerField()),
                ('label_name', models.CharField(max_length=255)),
                ('character', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.characteraudit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CharacterContact',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('contact_id', models.BigIntegerField()),
                ('contact_type', models.CharField(max_length=255)),
                ('standing', models.DecimalField(decimal_places=2, max_digits=4)),
                ('blocked', models.BooleanField(default=False)),
                ('watched', models.BooleanField(default=False)),
                ('character', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.characteraudit')),
                ('contact_name', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.evename')),
                ('labels', models.ManyToManyField(
                    to='corptools.CharacterContactLabel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
