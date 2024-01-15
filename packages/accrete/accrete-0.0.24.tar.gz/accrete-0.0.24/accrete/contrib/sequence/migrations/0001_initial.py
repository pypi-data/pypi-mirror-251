# Generated by Django 4.2.6 on 2023-10-10 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accrete', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('nextval', models.PositiveBigIntegerField(default=1, verbose_name='Next Value')),
                ('step', models.PositiveIntegerField(default=1, verbose_name='Step')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accrete.tenant')),
            ],
            options={
                'db_table': 'accrete_sequence',
            },
        ),
        migrations.AddConstraint(
            model_name='sequence',
            constraint=models.UniqueConstraint(fields=('name', 'tenant'), name='unique_name_per_tenant'),
        ),
        migrations.AddConstraint(
            model_name='sequence',
            constraint=models.UniqueConstraint(fields=('name', 'tenant', 'nextval'), name='unique_val_per_name_tenant'),
        ),
    ]
