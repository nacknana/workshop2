# Generated by Django 4.0.5 on 2022-06-24 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0006_contact_alter_invoiceitem_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('unread', 'ยังไม่ได้อ่าน'), ('readed', 'อ่านแล้ว')], default='unread', max_length=20),
        ),
    ]
