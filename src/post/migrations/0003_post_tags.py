# Generated by Django 2.2.16 on 2020-12-28 06:11

from django.db import migrations
import tag.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=tag.fields.PostTagField(default=dict(Tag=[])),
            preserve_default=False,
        ),
    ]
