# Generated by Django 5.0.6 on 2024-06-04 07:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='IsDeleted',
            new_name='is_deleted',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='updatedAt',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='category_ID',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='IsDeleted',
            new_name='is_deleted',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='updatedAt',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='options',
            old_name='category_ID',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='options',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='options',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='options',
            old_name='IsDeleted',
            new_name='is_deleted',
        ),
        migrations.RenameField(
            model_name='options',
            old_name='name',
            new_name='option_name',
        ),
        migrations.RenameField(
            model_name='options',
            old_name='updatedAt',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='IsDeleted',
            new_name='is_deleted',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Membership_ID',
            new_name='membership_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='updatedAt',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='order_amount',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='order_amount',
            old_name='IsDeleted',
            new_name='is_deleted',
        ),
        migrations.RenameField(
            model_name='order_amount',
            old_name='menu_ID',
            new_name='menu_id',
        ),
        migrations.RenameField(
            model_name='order_amount',
            old_name='ID',
            new_name='order_amount_id',
        ),
        migrations.RenameField(
            model_name='order_amount',
            old_name='updatedAt',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='order_menu',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='order_menu',
            old_name='Menu_ID',
            new_name='menu_id',
        ),
        migrations.RenameField(
            model_name='order_menu',
            old_name='Order_ID',
            new_name='order_id',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='owner_ID',
        ),
        migrations.RemoveField(
            model_name='options',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='options',
            name='order_menu_ID',
        ),
        migrations.AddField(
            model_name='category',
            name='owner_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='category',
            table='Category',
        ),
        migrations.AlterModelTable(
            name='menu',
            table='Menu',
        ),
        migrations.AlterModelTable(
            name='options',
            table='Options',
        ),
        migrations.CreateModel(
            name='OptionChoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('choice_name', models.CharField(max_length=100)),
                ('extra_cost', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('option_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='order.options')),
            ],
            options={
                'db_table': 'Option_choice',
            },
        ),
        migrations.CreateModel(
            name='Order_choice_order_menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('option_choice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.optionchoice')),
                ('order_menu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order_menu')),
            ],
            options={
                'db_table': 'Order_choice_order_menu',
            },
        ),
    ]
