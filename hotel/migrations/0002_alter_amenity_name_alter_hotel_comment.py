# Generated by Django 4.2.3 on 2024-03-09 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='comment',
            field=models.ManyToManyField(blank=True, to='hotel.comments'),
        ),
    ]