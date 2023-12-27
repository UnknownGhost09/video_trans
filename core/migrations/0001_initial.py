# Generated by Django 5.0 on 2023-12-12 12:40

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConvertedVideo",
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
                (
                    "videofile",
                    models.FileField(
                        null=True, upload_to="converted/", verbose_name=""
                    ),
                ),
                ("type", models.CharField(max_length=200)),
            ],
            options={
                "db_table": "convertedvideo",
            },
        ),
        migrations.CreateModel(
            name="Video",
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
                (
                    "videofile",
                    models.FileField(null=True, upload_to="videos/", verbose_name=""),
                ),
            ],
            options={
                "db_table": "video",
            },
        ),
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("verified_at", models.CharField(default="False", max_length=200)),
                ("role", models.CharField(default="user", max_length=200)),
                ("status", models.CharField(default="1", max_length=20)),
                (
                    "updated_at",
                    models.CharField(
                        default=datetime.datetime(2023, 12, 12, 18, 10, 39, 544526),
                        max_length=200,
                    ),
                ),
                (
                    "created_at",
                    models.CharField(
                        default=datetime.datetime(2023, 12, 12, 18, 10, 39, 544526),
                        max_length=200,
                    ),
                ),
                ("remember_token", models.CharField(default="False", max_length=200)),
                ("referal_by", models.CharField(max_length=200, null=True)),
                (
                    "referal_code",
                    models.CharField(default="0000", max_length=200, unique=True),
                ),
                ("phone_no", models.CharField(max_length=200, null=True)),
                ("activation_date", models.CharField(default="N/A", max_length=200)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "db_table": "users",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Transcript",
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
                ("script", models.TextField(null=True)),
                (
                    "c_id",
                    models.ForeignKey(
                        db_column="c_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.convertedvideo",
                    ),
                ),
                (
                    "video_id",
                    models.ForeignKey(
                        db_column="video_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.video",
                    ),
                ),
            ],
            options={
                "db_table": "transcript",
            },
        ),
        migrations.AddField(
            model_name="convertedvideo",
            name="video_id",
            field=models.ForeignKey(
                db_column="video_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="core.video",
            ),
        ),
    ]