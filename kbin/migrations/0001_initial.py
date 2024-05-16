# Generated by Django 5.0.4 on 2024-05-16 16:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_likes', models.PositiveIntegerField(default=0)),
                ('num_dislikes', models.PositiveIntegerField(default=0)),
                ('title', models.TextField(default='', max_length=25500)),
                ('body', models.TextField(max_length=35000, null=True)),
                ('creation_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_coments', models.PositiveIntegerField(default=0)),
                ('num_boosts', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=25000, unique=True)),
                ('title', models.CharField(max_length=50000)),
                ('description', models.TextField(max_length=40000, null=True)),
                ('rules', models.TextField(max_length=10000, null=True)),
                ('nsfw', models.BooleanField(null=True)),
                ('n_threads', models.PositiveIntegerField(default=0)),
                ('n_links', models.PositiveIntegerField(default=0)),
                ('n_elements', models.PositiveIntegerField(default=0)),
                ('n_suscriptions', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('description', models.TextField(default='', max_length=10000)),
                ('cover', models.ImageField(default='', max_length=10000, upload_to='')),
                ('avatar', models.ImageField(default='', max_length=10000, upload_to='')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('api_key', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('publicacio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kbin.publicacio')),
                ('url', models.TextField(default='', max_length=35000)),
            ],
            bases=('kbin.publicacio',),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('publicacio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kbin.publicacio')),
            ],
            bases=('kbin.publicacio',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=35000, null=True)),
                ('creation_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edited', models.DateTimeField(null=True)),
                ('num_likes', models.PositiveIntegerField(default=0)),
                ('num_dislikes', models.PositiveIntegerField(default=0)),
                ('level', models.PositiveIntegerField(default=1)),
                ('thread', models.ForeignKey(default='default_thread', on_delete=django.db.models.deletion.CASCADE, to='kbin.publicacio')),
                ('author', models.ForeignKey(default='default_user', on_delete=django.db.models.deletion.CASCADE, to='kbin.user')),
            ],
        ),
        migrations.AddField(
            model_name='publicacio',
            name='magazine',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='kbin.magazine'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('magazine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.magazine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.user')),
            ],
        ),
        migrations.AddField(
            model_name='publicacio',
            name='author',
            field=models.ForeignKey(default='default_user', on_delete=django.db.models.deletion.CASCADE, to='kbin.user'),
        ),
        migrations.AddField(
            model_name='magazine',
            name='author',
            field=models.ForeignKey(default='default_user', on_delete=django.db.models.deletion.CASCADE, to='kbin.user'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_comments', to='kbin.comment')),
                ('comment_root', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='root_comments', to='kbin.comment')),
            ],
            options={
                'unique_together': {('comment_root', 'comment_reply')},
            },
        ),
        migrations.CreateModel(
            name='Boost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publicacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.publicacio')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.user')),
            ],
            options={
                'unique_together': {('user', 'publicacio')},
            },
        ),
        migrations.CreateModel(
            name='Vot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positiu', models.BooleanField()),
                ('publicacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.publicacio')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.user')),
            ],
            options={
                'unique_together': {('user', 'publicacio')},
            },
        ),
        migrations.CreateModel(
            name='Vote_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(default='like')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbin.user')),
            ],
            options={
                'unique_together': {('comment', 'user')},
            },
        ),
    ]
