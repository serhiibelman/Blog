# Generated by Django 2.0.3 on 2018-03-21 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_article_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(default=None, verbose_name='date published'),
            preserve_default=False,
        ),
    ]