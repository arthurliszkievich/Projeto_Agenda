# Generated by Django 5.1.7 on 2025-03-31 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0006_alter_category_options_contact_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
