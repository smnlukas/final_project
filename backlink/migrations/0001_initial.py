# Generated by Django 3.2.19 on 2023-06-27 16:51

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('available_articles', models.IntegerField(default=0)),
                ('bio', models.TextField()),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Vartotojas',
                'verbose_name_plural': 'Vartotojai',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Kategorija',
                'verbose_name_plural': 'Kategorijos',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('price', models.FloatField()),
                ('articles_number', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Produktas',
                'verbose_name_plural': 'Produktai',
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('website_id', models.AutoField(primary_key=True, serialize=False)),
                ('website_url', models.CharField(max_length=50, unique=True)),
                ('category', models.ManyToManyField(to='backlink.Category')),
            ],
            options={
                'verbose_name': 'Svetainė',
                'verbose_name_plural': 'Svetainės',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('content', ckeditor.fields.RichTextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backlink.category')),
                ('website', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backlink.website')),
            ],
            options={
                'verbose_name': 'Straipsnis',
                'verbose_name_plural': 'Straipsniai',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='ArticleOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20, unique=True)),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('bank_account_number', models.CharField(max_length=34)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.IntegerField(choices=[(0, 'Waiting'), (1, 'Paid'), (2, 'Canceled')], default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='backlink.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Straipsnių užsakyai',
                'verbose_name_plural': 'Straipsnių užsakymai',
            },
        ),
    ]
