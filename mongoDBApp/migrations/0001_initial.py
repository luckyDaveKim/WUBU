# Generated by Django 4.1 on 2024-02-11 06:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MatchedRulesModel",
            fields=[
                (
                    "code",
                    models.CharField(max_length=6, primary_key=True, serialize=False),
                ),
                ("analysis_date", models.DateField()),
                ("rules", models.JSONField()),
            ],
            options={
                "db_table": "matched_rules",
                "unique_together": {("code", "analysis_date")},
            },
        ),
    ]