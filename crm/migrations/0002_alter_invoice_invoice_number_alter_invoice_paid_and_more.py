# Generated by Django 4.2 on 2023-05-02 10:01

import crm.models.invoice
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, default=crm.models.invoice._generate_new_invoice_number, editable=False, max_length=9, validators=[crm.models.invoice._validate_new_number]),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='crm.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]