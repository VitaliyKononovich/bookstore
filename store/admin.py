from django.contrib import admin
from .models import Book, Author, BookOrder, Cart, Review


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')


class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'cart', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active', 'order_date')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id',  'book', 'user', 'publish_date')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookOrder, BookOrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Review, ReviewAdmin)

