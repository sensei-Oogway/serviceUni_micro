# Generated by Django 4.2.5 on 2023-10-17 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("subject_code", models.CharField(default="ABC123", max_length=20)),
                ("name", models.CharField(max_length=255)),
                ("details", models.TextField(default="No details available")),
            ],
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("user", models.IntegerField()),
                ("subjects", models.ManyToManyField(to="student_app.subject")),
            ],
        ),
    ]
