from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from .throttles import TenCallsPerMinute
from django.contrib.auth.models import User, Group

# ============================MENU=============================================
@api_view(['GET','POST','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        # filtering
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title__iexact=category_name)
            # double underscore is necessary
            # case sensitive => solved by adding __iexact cf. field lookups
            # /api/menu-items/?category=soup => because of ... .get('category')
        if to_price:
            items = items.filter(price=to_price)
            # __lte => less than, or equal to the value
            # if you want exact price do not use __lte
            # /api/menu-items/?to_price=15 => because of ... .get('to_price')
        if search:
            items = items.filter(title__contains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
            # /api/menu-items/?ordering=-price => desc / price asc
            # example: /api/menu-items/?ordering=price&category=soup
        # pagination
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
            # /api/menu-items/?perpage=3&page=2
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True)
        # many=True is essential arg. because it converts the list to the json data when you want to return single object, do not use
        return Response(serialized_item.data)
    if request.method in ['POST','PUT','PATCH']:
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.remove()
            return Response(serialized_item.data, status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view()
@throttle_classes([TenCallsPerMinute])
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)
# ============================MENU=============================================


# ========================MANAGER GROUP MANAGEMENT=============================
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def managers(request):
    user = request.user
    manager_group = Group.objects.get(name="Manager")
    if user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            manager_users = manager_group.user_set.all()
            usernames = [u.username for u in manager_users]
            return Response(usernames, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            username = request.data.get('username')
            if username:
                new_manager = User.objects.get(username=username)
                manager_group.user_set.add(new_manager)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Please provide a valid username"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def single_user(request, user_id):
    user = request.user
    if user.groups.filter(name='Manager').exists():    
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        manager_group = Group.objects.get(name='Manager')
        if manager_group in user.groups.all():
            user.groups.remove(manager_group)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
# ========================MANAGER GROUP MANAGEMENT=============================


# =====================DELIVERY CREW GROUP MANAGEMENT==========================
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def delivery_crew(request):
    user = request.user
    delivery_crew_group = Group.objects.get(name='Delivery crew')
    if user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            delivery_crew_users = delivery_crew_group.user_set.all()
            usernames = [u.username for u in delivery_crew_users]
            return Response(usernames, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            username = request.data.get('username')
            if username:
                new_delivery_crew = User.objects.get(username=username)
                delivery_crew_group.user_set.add(new_delivery_crew)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Please provide a valid username"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def single_delivery_crew(request, user_id):
    user = request.user
    if user.groups.filter(name='Manager').exists():    
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        delivery_crew_group = Group.objects.get(name='Delivery crew')
        if delivery_crew_group in user.groups.all():
            user.groups.remove(delivery_crew_group)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
# =====================DELIVERY CREW GROUP MANAGEMENT==========================


# ===============================CART==========================================
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def cart_items(request):
    if request.method == 'GET':
        if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery crew").exists():
            items = Cart.objects.all()
            serialized_item = CartSerializer(items, many=True)
            return Response(serialized_item.data)
        else: 
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'POST':
        if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery crew").exists():
            serialized_item = CartSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'DELETE':
        if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery crew").exists():
            serialized_item = CartSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.delete()
            return Response(serialized_item.data, status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
# ===============================CART==========================================


# ================================ORDER========================================
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def order(request):
    if request.method == 'GET':
        items = OrderItem.objects.all()
        serialized_item = OrderItemSerializer(items, many=True)
        return Response(serialized_item.data)
    elif request.method == 'POST':
        if not (request.user.groups.filter(name="Manager").exists() or request.user.groups.filter(name="Delivery crew").exists()):
            serialized_item = OrderItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def single_order(request, order_id):
    item = get_object_or_404(OrderItem, pk=order_id)
    serialized_item = OrderItemSerializer(item)
    if not request.user.groups.filter(name="Manager").exists() and not request.user.groups.filter(name="Delivery crew").exists():
        if request.method == 'GET':
            return Response(serialized_item.data)
        elif request.method in ['PUT','PATCH']:
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
    elif request.user.groups.filter(name="Manager").exists():
        if request.method == 'DELETE':
            serialized_item.is_valid(raise_exception=True)
            serialized_item.delete()
            return Response(serialized_item.data, status.HTTP_204_NO_CONTENT)
    elif request.user.groups.filter(name="Delivery crew").exists():
        if request.method == 'PATCH':
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
    else:
        return Response(status.HTTP_401_UNAUTHORIZED)
# ================================ORDER========================================


# =====================TOKEN-BASED AUTHENTICATION==============================
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"You got the secret message"})

@api_view()
@permission_classes(IsAuthenticated)
def me(request):
    return Response(request.user.username)
# =====================TOKEN-BASED AUTHENTICATION==============================


# ==========================MANAGER VIEW=======================================
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"You're world's best boss"})
    else:
        return Response({"message":"You're not authorized"}, 403)
# ==========================MANAGER VIEW=======================================


# ============================THROTTLING=======================================
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"This message is only displayed to logged in users"})
# ============================THROTTLING=======================================



