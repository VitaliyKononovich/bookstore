from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


def cover_upload_path(instance, filename):
    return '/'.join(['books', str(instance.id), filename])


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    description = models.TextField(default='')
    publish_date = models.DateField(default=timezone.now)

    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField(default=0)

    # cover_image = models.ImageField(upload_to='books/', default='books/empty_cover.jpg')
    cover_image = models.ImageField(upload_to=cover_upload_path, default='books/empty_cover.jpg')

    def __str__(self):
        return f'"{self.title}" by {self.author}'


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publish_date = models.DateField(default=timezone.now)
    text = models.TextField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    order_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)

    def add_to_cart(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            preexisiting_order = BookOrder.objects.get(book=book, cart=self)
            preexisiting_order.quantity += 1
            preexisiting_order.save()
        except BookOrder.DoesNotExist:
            new_order = BookOrder.objects.create(book=book, cart=self, quantity=1)
            new_order.save()

    def remove_from_cart(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            preexisiting_order = BookOrder.objects.get(book=book, cart=self)
            if preexisiting_order.quantity > 1:
                preexisiting_order.quantity -= 1
                preexisiting_order.save()
            else:
                preexisiting_order.delete()
        except BookOrder.DoesNotExist:
            pass

    def __str__(self):
        return f'Cart {self.id} for {self.user} ({self.active})'


class BookOrder(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()