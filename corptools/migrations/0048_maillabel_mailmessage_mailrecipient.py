# Generated by Django 3.2.5 on 2021-07-13 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corptools', '0047_auto_20210531_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailLabel',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('label_id', models.IntegerField(default=None)),
                ('label_name', models.CharField(
                    default=None, max_length=255, null=True)),
                ('label_color', models.CharField(
                    default=None, max_length=7, null=True)),
                ('unread_count', models.IntegerField(default=None, null=True)),
                ('character', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.characteraudit')),
            ],
        ),
        migrations.CreateModel(
            name='MailRecipient',
            fields=[
                ('recipient_id', models.BigIntegerField(
                    primary_key=True, serialize=False, unique=True)),
                ('recipient_type', models.CharField(choices=[('alliance', 'alliance'), ('character', 'character'), (
                    'corporation', 'corporation'), ('mailing_list', 'mailing_list')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='MailMessage',
            fields=[
                ('id_key', models.BigIntegerField(
                    primary_key=True, serialize=False, unique=True)),
                ('mail_id', models.IntegerField(default=None, null=True)),
                ('from_id', models.IntegerField(default=None, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(default=None, null=True)),
                ('subject', models.CharField(default=None, max_length=255, null=True)),
                ('body', models.CharField(default=None, max_length=12000, null=True)),
                ('character', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='corptools.characteraudit')),
                ('labels', models.ManyToManyField(to='corptools.MailLabel')),
                ('recipients', models.ManyToManyField(
                    to='corptools.MailRecipient')),
            ],
        ),
    ]
