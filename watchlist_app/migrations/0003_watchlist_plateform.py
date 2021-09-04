# Generated by Django 3.2.3 on 2021-06-02 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0002_auto_20210602_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='plateform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='watchlist_app.streamplateform'),
            preserve_default=False,
        ),
    ]
