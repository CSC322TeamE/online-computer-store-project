# Generated by Django 2.2.5 on 2021-05-02 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineComputerStore', '0027_auto_20210502_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverycompany',
            name='name',
        ),
        migrations.RemoveField(
            model_name='deliverycompany',
            name='price',
        ),
        migrations.RemoveField(
            model_name='deliverycompany',
            name='rating',
        ),
        migrations.AlterField(
            model_name='discussion',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineComputerStore.Forum'),
        ),
        migrations.CreateModel(
            name='Bidfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('delivery_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineComputerStore.DeliveryCompany')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineComputerStore.Order')),
            ],
        ),
    ]
