# Generated by Django 2.2.5 on 2021-04-30 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineComputerStore', '0003_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='img',
            field=models.ImageField(default='default_img/400x650.png', height_field=650, upload_to='item_img', width_field=400),
        ),
    ]
