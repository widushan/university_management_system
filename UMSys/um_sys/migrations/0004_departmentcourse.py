# Generated by Django 5.2.1 on 2025-06-11 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("um_sys", "0003_lecturer_lecturemodule"),
    ]

    operations = [
        migrations.CreateModel(
            name="DepartmentCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("course_id", models.CharField(max_length=20)),
                ("course_name", models.CharField(max_length=100)),
                (
                    "degree",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="um_sys.degree"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="um_sys.department",
                    ),
                ),
            ],
        ),
    ]
