# Generated by Django 3.2.3 on 2021-06-03 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0004_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='watchlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='watchlist_app.watchlist'),
        ),
    ]