# Generated by Django 2.2 on 2020-01-11 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200111_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.CategoryProduct'),
        ),
    ]
