# Generated by Django 3.2.25 on 2024-07-03 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20211130_2003'),
        ('quest_manager', '0034_alter_questsubmission_quest'),
    ]

    operations = [
        migrations.AddField(
            model_name='questsubmission',
            name='draft_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='comments.comment'),
        ),
    ]
