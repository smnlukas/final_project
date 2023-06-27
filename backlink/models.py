from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max


def bank_account_validator(value):
    if not value.startswith("LT"):
        raise ValidationError("Banko sąskaitos numeris turi prasidėti 'LT'")

    def __str__(self):
        return f"{self.order_number} - {self.product.name} - {self.product.price}"

class User(AbstractUser):
    available_articles = models.IntegerField(default=0)
    bio = models.TextField()
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='custom_user_permissions')

    def update_available_articles(self):
        total_articles = self.articleorder_set.aggregate(total_articles=models.Sum('product__articles_number'))['total_articles']
        self.available_articles = total_articles or 0
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price= models.FloatField()
    articles_number = models.IntegerField(default=0)

PAYMENT = (
    (0,"Waiting"),
    (1,"Paid"),
    (2,"Canceled")
)

class ArticleOrder(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    bank_account_number = models.CharField(max_length=34, null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.IntegerField(choices=PAYMENT, default=0)

    def save(self, *args, **kwargs):
        if not self.order_number:  # Only generate order number if it's not set
            max_order_number = ArticleOrder.objects.aggregate(max_order_number=Max('order_number'))['max_order_number']
            if max_order_number:
                current_order_number = int(max_order_number)
                self.order_number = str(current_order_number + 1).zfill(5)  # Increment and format order number
            else:
                self.order_number = '00001'  # Initial order number

        super().save(*args, **kwargs)
        self.user.update_available_articles()


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name

class Website(models.Model):
    website_id = models.AutoField(primary_key=True)
    website_url = models.CharField(max_length=50, unique=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.website_url

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('backlink.User', on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    website = models.ForeignKey(Website, on_delete=models.SET_NULL, null=True)
    category= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS, default=0)


    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


