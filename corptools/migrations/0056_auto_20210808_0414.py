# Generated by Django 3.2.5 on 2021-08-08 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corptools', '0055_alter_characterroles_character'),
    ]

    operations = [
        migrations.AddField(
            model_name='charactertitle',
            name='corporation_name',
            field=models.CharField(max_length=500),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Titlefilter',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('titles', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.charactertitle')),
            ],
            options={
                'verbose_name': 'Smart Filter: Corporate Role checks',
                'verbose_name_plural': 'Smart Filter: Corporate Role checks',
            },
        ),
    ]
