# Generated by Django 3.2.4 on 2022-11-28 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0004_boundary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sacepconfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.PositiveIntegerField(choices=[(0, 'Deleted'), (2, 'Active'), (3, 'Inactive')], default=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deactivation_date', models.DateTimeField(blank=True, null=True)),
                ('art_center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='art_center_tagged', to='master_data.boundary')),
                ('sacep', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sacep_tagged', to='master_data.boundary')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
