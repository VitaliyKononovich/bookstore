from django.test import TestCase
from.models import Book, Author
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *


class StoreViewsTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(first_name='Stephen', last_name='King')
        book = Book.objects.create(title='Cujo', author=author, description='Darn scary!', price=9.99, stock=1)
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@my.com',
            password='prikolis'
        )

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_index(self):
        resp = self.client.get('/store/')
        self.assertEqual(resp.status_code, 200)   # 200 - OK
        self.assertTrue('books' in resp.context)
        print(resp.context['books'].count())
        self.assertTrue(resp.context['books'].count() > 0)

    def test_cart(self):
        resp = self.client.get('/store/cart/')
        self.assertEqual(resp.status_code, 302)  # 302 - Redirect

    def test_book_detail(self):
        resp = self.client.get('/store/book/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['book'].pk, 1)
        self.assertEqual(resp.context['book'].title, 'Cujo')

        resp = self.client.get('/store/book/2/')
        self.assertEqual(resp.status_code, 404)

    def test_add_to_cart(self):
        self.logged_in = self.client.login(username='test_user', password='prikolis')
        self.assertTrue(self.logged_in)
        self.client.get('/store/add/1/')
        resp = self.client.get('/store/cart/')
        self.assertEqual(resp.context['total'], Decimal('9.99'))
        self.assertEqual(resp.context['count'], 1)
        self.assertEqual(resp.context['cart'].count(), 1)
        self.assertEqual(resp.context['cart'].get().quantity, 1)