# Generated by Django 4.2.4 on 2023-08-17 21:23

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
            name="l_Info",
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
                    "l_category",
                    models.CharField(
                        choices=[
                            ("PC", "PC"),
                            ("닌텐도", "닌텐도"),
                            ("플스", "플스"),
                            ("엑스박스", "엑스박스"),
                            ("기타", "기타"),
                        ],
                        default="news",
                        max_length=64,
                        verbose_name="카테고리",
                    ),
                ),
                ("l_title", models.CharField(max_length=128, verbose_name="제목")),
                ("l_contents", models.TextField(verbose_name="내용")),
                (
                    "l_register_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="등록날짜"
                    ),
                ),
                ("l_click", models.PositiveIntegerField(default=0)),
                ("l_votes", models.PositiveIntegerField(default=0)),
                (
                    "l_voters",
                    models.ManyToManyField(
                        blank=True, related_name="upvoted_infos", to="bcuser.bcuser"
                    ),
                ),
                (
                    "l_writer",
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
            name="l_Comment",
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
                ("l_comment", models.CharField(max_length=256, verbose_name="댓글 내용")),
                (
                    "l_created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="작성일"),
                ),
                (
                    "l_author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bcuser.bcuser",
                        verbose_name="작성자",
                    ),
                ),
                (
                    "l_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="l_info.l_info",
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