from django.contrib import admin
from .models import Post,Category,Website,ArticleOrder,Product, User


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class ArticleOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'product', 'user','payment')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'articles_number')

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('website_url',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(ArticleOrder, ArticleOrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
