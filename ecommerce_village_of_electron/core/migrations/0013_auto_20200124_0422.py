# Generated by Django 2.2 on 2020-01-24 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_checkoutmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttags',
            name='tag_product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Item'),
        ),
    ]
