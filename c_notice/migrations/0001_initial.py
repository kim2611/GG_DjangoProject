# Generated by Django 4.2.4 on 2023-08-18 11:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("bcuser", "0002_bcuser_nickname"),
    ]

    operations = [
        migrations.CreateModel(
            name="c_Notice",
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
                    "c_category",
                    models.CharField(
                        choices=[("공지", "공지"), ("이벤트", "이벤트"), ("기타", "기타")],
                        default="news",
                        max_length=64,
                        verbose_name="카테고리",
                    ),
                ),
                ("c_title", models.CharField(max_length=128, verbose_name="제목")),
                ("c_contents", models.TextField(verbose_name="내용")),
                (
                    "c_register_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="등록날짜"
                    ),
                ),
                ("c_click", models.PositiveIntegerField(default=0)),
                ("c_votes", models.PositiveIntegerField(default=0)),
                (
                    "c_voters",
                    models.ManyToManyField(
                        blank=True, related_name="upvoted_notices", to="bcuser.bcuser"
                    ),
                ),
                (
                    "c_writer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bcuser.bcuser",
                        verbose_name="작성자",
                    ),
                ),
            ],
            options={
                "verbose_name": "게임정보글",
                "verbose_name_plural": "게임정보 게시판",
            },
        ),
        migrations.CreateModel(
            name="c_Comment",
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
                ("comment", models.CharField(max_length=256, verbose_name="댓글 내용")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="작성일"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bcuser.bcuser",
                        verbose_name="작성자",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="c_notice.c_notice",
                        verbose_name="게시글",
                    ),
                ),
            ],
            options={
                "verbose_name": "댓글",
                "verbose_name_plural": "댓글들",
            },
        ),
    ]