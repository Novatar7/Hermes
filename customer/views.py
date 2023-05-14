from django.shortcuts import render
from django.http import request
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel

from customer.models import MenuItem, OrderModel

# Create your views here.
class Index(View):
    def get(self, request,*args, **kwargs):
        return render(request, 'customer/Index.html')

class About(View):
    def get(self, request,*args, **kwargs):
        return render(request, 'customer/About.html')
    
class Order(View):
    def get(self, request, *args, **kwargs):
        pass
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        maincourse = MenuItem.objects.filter(category__name__contains='Main course')
        sides = MenuItem.objects.filter(category__name__contains='Sides')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')

        # pass into context
        context = {
            'appetizers': appetizers,
            'maincourse' : maincourse,
            'sides' : sides,
            'drinks' : drinks,
        }
        # render the template
        return render(request,'customer/order.html', context)
    
    def post (self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        order_items={
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item)) 
            item_data ={
                'id' : menu_item.pk,
                'name' :menu_item.name,
                'price' :menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            address=address
            )

        order.items.add(*item_ids)

        # After everything is done, send confirmation email to customer 
        body =('Thank you for your order! It will be delivered Soon!!\n'
        f'Your total:{price}\n'
        'We will get to you soon!')
        
        send_mail(
            'Thank You For Order!
            body,
            'example@gmail.com',
            [email],
            fail_silently=False
        )

        context ={
                'items' : order_items['items'],
                'price' : price

        }
        return render(request,'customer/order_confirmation.html')
        
