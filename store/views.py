from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Cart, BookOrder, Review
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
import paypalrestsdk
import stripe
from django.conf import settings
from random import randint, choice

from .forms import ReviewForm

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
import string

from . import signals

import logging
logger = logging.getLogger(__name__)


def index(request):
    return redirect('store:index')


def store(request):
    """count = Book.objects.all().count()
    context = {'count': count}
    request.session['location'] = 'unknown'
    if request.user.is_authenticated:
        request.session['location'] = 'Earth'"""
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'base.html', context=context)


def book_details(request, book_id):
    # book = Book.objects.get(pk=book_id)
    book = get_object_or_404(Book, id=book_id)
    context = {'book': book}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = Review.objects.create(
                    user=request.user,
                    book=context['book'],
                    text=form.cleaned_data.get('text')
                )
                new_review.save()

                # Prepare and send message with discount
                if Review.objects.filter(user=request.user).count() < 6:
                    subject = 'Your MysteryBooks.com discount code is here!'
                    from_email = 'librarian@mysterybooks.com'
                    to_email = [request.user.email]

                    email_context = Context({
                        'username': request.user.username,
                        'code': ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                        'discount': 10
                    })
                    text_email = render_to_string('email/review_email.txt', email_context)
                    html_email = render_to_string('email/review_email.html', email_context)

                    msg = EmailMultiAlternatives(subject, text_email, from_email, to_email)
                    msg.attach_alternative(html_email, 'text/html')
                    msg.content_subtype = 'html'
                    msg.send()

        else:
            if Review.objects.filter(user=request.user, book=context['book']).count() == 0:
                form = ReviewForm()
                context['form'] = form
        context['reviews'] = book.review_set.all()
    return render(request, 'store/detail.html', context=context)


def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(user=request.user, active=True)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user)
                cart.save()
            cart.add_to_cart(book_id)
        return redirect('store:cart')
    else:
        return redirect('store:index')


def remove_from_cart(request, book_id):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_from_cart(book_id)
        return redirect('store:cart')
    else:
        return redirect('store:index')


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, active=True)
        if cart:
            orders = BookOrder.objects.filter(cart=cart[0])
        else:
            orders = []
        total, count = 0, 0
        for order in orders:
            total += (order.book.price * order.quantity)
            count += order.quantity
        context = {
            'cart': orders,
            'total': total,
            'count': count
        }
        return render(request, 'store/cart.html', context)
    else:
        return redirect('index')


def checkout(request, processor):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, active=True)
        if cart:
            orders = BookOrder.objects.filter(cart=cart[0])
        else:
            orders = []
        if processor == 'paypal':
            redirect_url = checkout_paypal(request, cart, orders)
            return redirect(redirect_url)
        elif processor == 'stripe':
            token = request.POST['stripeToken']
            status = checkout_stripe(cart, orders, token)
            if status:
                return redirect(reverse('store:process_order', args=['stripe']))
            else:
                return redirect('store:order_error', context={'message': 'There was a problem processing your payment.'})
        else:
            return redirect('store:index')


def checkout_paypal(request, cart, orders):
    if request.user.is_authenticated:
        items, total = [], 0
        for order in orders:
            total += (order.book.price * order.quantity)
            book = order.book
            item = {
                'name': book.title,
                'sku': book.id,
                'price': str(book.price),
                'currency': 'USD',
                'quantity': order.quantity
            }
            items.append(item)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        paypalrestsdk.configure({
            'mode': 'sandbox',
            'client_id': settings.PAYPAL['client_id'],
            'client_secret': settings.PAYPAL['client_secret']
        })
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {'payer_method': 'paypal'},
            'redirect_urls': {
                'return_url': settings.PAYPAL['return_url'],
                'cancel_url': settings.PAYPAL['cancel_url']
            },
            'transactions': [{
                'item_list': {'items': items},
                'amount': {'total': str(total), 'currency': 'USD'},
                'description': 'Mystery Book order.'}]
        })
        if payment.create():
            cart_instance = cart.get()
            cart_instance.payment_id = payment.id
            cart_instance.save()
            for link in payment.links:
                if link.method == 'REDIRECT':
                    redirect_url = str(link.href)
                    return redirect_url
        else:
            return reverse('store:order_error')

        # dummy block instead above one
        # cart_instance = cart.get()
        # cart_instance.payment_id = randint(1000, 100000)
        # cart_instance.save()
        # return f'http://127.0.0.1:8000/store/process/paypal?paymentId={cart_instance.payment_id}&token=as-is&PayerID=2020'

    else:
        return redirect('store:index')


def checkout_stripe(cart, orders, token):
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Insert here your api_key
    stripe.api_key = ""
    total = 0
    for order in orders:
        total += (order.book.price * order.quantity)
    status = True
    try:
        change = stripe.Charge.create(
            amount=int(total * 100),
            currency='USD',
            source=token,
            metadata={'order_id': cart.get().id}
        )
        cart_instance = cart.get()
        cart_instance.payment_id = change.id
        cart_instance.save()
    except stripe.error.CardError as e:
        status = False
    return status


def order_error(request):
    if request.user.is_authenticated:
        return render(request, 'store/order_error.html')
    else:
        return redirect('store:index')


def process_order(request, processor):
    if request.user.is_authenticated:
        if processor == 'paypal':
            payment_id = request.GET.get('paymentId')
            cart = Cart.objects.filter(payment_id=payment_id)
            if cart:
                orders = BookOrder.objects.filter(cart=cart[0])
            else:
                orders = []
            total = 0
            for order in orders:
                total += (order.book.price * order.quantity)
            context = {
                'cart': orders,
                'total': total,
            }
            return render(request, 'store/process_order.html', context)
        elif processor == 'stripe':
            return JsonResponse({'redirect_url': reverse('store:complete_order', args=['stripe'])})
    else:
        return redirect('store:index')


def complete_order(request, processor):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, active=True)
        if processor == 'paypal':
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            payment = paypalrestsdk.Payment.find(cart.payment_id)
            if payment.execute({'payer_id': payment.payer_info.payer_id}):
                message = f'Success! Your order has been completed and is being processed. Payment ID: {payment.id}'
                cart.active = False
                cart.order_date = timezone.now()
                cart.payment_type = processor
                cart.save()
            else:
                message = f'There was a problem with the transaction. Error: {payment.error.message}'
            context = {'message': message}

            # dummy block instead above one
            # context = {'message': f'Success! Your order has been completed and is being processed. Payment ID: {cart.payment_id}'}
            # cart.active = False
            # cart.order_date = timezone.now()
            # cart.payment_type = processor
            # cart.save()

            return render(request, 'store/order_complete.html', context)
        elif processor == 'stripe':
            cart.active = False
            cart.order_date = timezone.now()
            cart.payment_type = processor
            cart.save()
            context = {'message': f'Success! Your order has been completed, and is being processed. Payment ID: {cart.payment_id}'}
            return render(request, 'store/order_complete.html', context)
    else:
        return redirect('store:index')
