# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 12:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, unique=True, verbose_name='Created on')),
                ('payment_no', models.PositiveIntegerField(editable=False, unique=True, verbose_name='Payment on')),
                ('payment_info', models.CharField(editable=False, max_length=128, verbose_name='Payment Info')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Amount')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'invoice',
                'verbose_name_plural': 'invoices',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Amount')),
                ('payment_no', models.PositiveIntegerField(unique=True, verbose_name='Payment no')),
                ('ik_pw_via', models.CharField(max_length=255, verbose_name='Payway Via')),
                ('ik_cur', models.CharField(max_length=3, verbose_name='Currency')),
                ('ik_inv_prc', models.DateTimeField(verbose_name='Invoice Processed')),
                ('invoice', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='interkassa_merchant.Invoice', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
            },
        ),
    ]