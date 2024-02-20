# Generated by Django 5.0.2 on 2024-02-20 08:04

import django.db.models.deletion
import shortuuid.django_fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "account_balance",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
                (
                    "account_number",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="1234567890",
                        length=10,
                        max_length=30,
                        prefix="154",
                        unique=True,
                    ),
                ),
                (
                    "account_id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="1234567890",
                        length=7,
                        max_length=25,
                        prefix="DEX",
                        unique=True,
                    ),
                ),
                (
                    "pin_number",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="1234567890",
                        length=4,
                        max_length=7,
                        prefix="",
                        unique=True,
                    ),
                ),
                (
                    "ref_code",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefh1234567890",
                        length=10,
                        max_length=30,
                        prefix="",
                        unique=True,
                    ),
                ),
                (
                    "account_status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("pending", "Pending"),
                            ("in-active", "In-active"),
                        ],
                        default="in-active",
                        max_length=100,
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("kyc_submitted", models.BooleanField(default=False)),
                ("kyc_confirmed", models.BooleanField(default=False)),
                (
                    "recommended_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="recommended_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="KYC",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("full_name", models.CharField(max_length=300)),
                ("image", models.ImageField(default="default.jpg", upload_to="kyc")),
                ("nationality", models.CharField(max_length=100)),
                (
                    "marital_status",
                    models.CharField(
                        choices=[
                            ("married", "Married"),
                            ("single", "Single"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                        ],
                        max_length=40,
                    ),
                ),
                (
                    "identity_type",
                    models.CharField(
                        choices=[
                            ("national_id_card", "National ID Card"),
                            ("drivers_licence", "Drives Licence"),
                            ("international_passport", "International Passport"),
                        ],
                        max_length=140,
                    ),
                ),
                (
                    "identity_image",
                    models.ImageField(blank=True, null=True, upload_to="kyc"),
                ),
                ("date_of_birth", models.DateTimeField()),
                ("signature", models.ImageField(upload_to="kyc")),
                ("country", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("mobile", models.CharField(max_length=12)),
                ("fax", models.CharField(max_length=12)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "account",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.account",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
