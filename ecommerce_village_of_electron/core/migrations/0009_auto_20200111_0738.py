# Generated by Django 2.2 on 2020-01-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_producttags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='producttags',
            name='tag_name',
        ),
        migrations.AddField(
            model_name='producttags',
            name='tag_name',
            field=models.ManyToManyField(to='core.Tag'),
        ),
    ]
