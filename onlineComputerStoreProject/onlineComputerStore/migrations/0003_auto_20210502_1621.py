# Generated by Django 2.2.5 on 2021-05-02 20:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('onlineComputerStore', '0002_auto_20210502_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.UUIDField(default=uuid.UUID('f5b2dedb-ab83-11eb-8d62-7824afca968b'), editable=False),
        ),
        migrations.CreateModel(
            name='Bidfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('deli_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineComputerStore.DeliveryCompany')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineComputerStore.Order')),
            ],
        ),
    ]
