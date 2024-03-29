# Generated by Django 4.2 on 2024-03-17 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api_refs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="referral",
            name="referral_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="referred_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
