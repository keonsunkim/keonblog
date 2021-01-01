# Generated by Django 2.2.16 on 2020-12-30 11:41

from django.db import migrations
import tag.fields
import tag.utils


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20201230_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=tag.fields.PostTagField(blank=True, default=tag.utils.post_tag_default_dict, null=True),
        ),
    ]
