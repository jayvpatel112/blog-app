# Generated by Django 4.0.4 on 2022-05-03 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allposts', '0003_comment_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='post',
        ),
    ]
