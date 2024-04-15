# Generated by Django 4.1.13 on 2024-04-15 14:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('title', models.TextField(default='', max_length=255)),
                ('body', models.TextField(max_length=35000, null=True)),
                ('creation_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_coments', models.PositiveIntegerField(default=0)),
                ('num_boosts', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('cover', models.ImageField(upload_to='')),
                ('avatar', models.ImageField(upload_to='')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('publicacio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.publicacio')),
                ('url', models.TextField(default='', max_length=35000)),
            ],
            bases=('api.publicacio',),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('publicacio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.publicacio')),
            ],
            bases=('api.publicacio',),
        ),
        migrations.AddField(
            model_name='publicacio',
            name='author',
            field=models.ForeignKey(default='default_user', on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=25)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=10000, null=True)),
                ('rules', models.TextField(max_length=10000, null=True)),
                ('nsfw', models.BooleanField(null=True)),
                ('n_threads', models.PositiveIntegerField(default=0)),
                ('n_comments', models.PositiveIntegerField(default=0)),
                ('n_links', models.PositiveIntegerField(default=0)),
                ('n_elements', models.PositiveIntegerField(default=0)),
                ('n_suscriptions', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(default='default_user', on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=35000, null=True)),
                ('creation_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_likes', models.PositiveIntegerField(default=0)),
                ('num_dislikes', models.PositiveIntegerField(default=0)),
                ('level', models.PositiveIntegerField(default=1)),
                ('author', models.ForeignKey(default='default_user', on_delete=django.db.models.deletion.CASCADE, to='api.user')),
                ('thread', models.ForeignKey(default='default_thread', on_delete=django.db.models.deletion.CASCADE, to='api.publicacio')),
            ],
        ),
        migrations.CreateModel(
            name='Vote_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(default='like')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
            options={
                'unique_together': {('comment', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_comments', to='api.comment')),
                ('comment_root', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='root_comments', to='api.comment')),
            ],
            options={
                'unique_together': {('comment_root', 'comment_reply')},
            },
        ),
    ]
