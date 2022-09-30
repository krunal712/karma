from django.shortcuts import render,redirect
from django.db.models import Count
from .models import Products,Category,Users,Login,login_required,Cart
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import serializers
import jwt
import datetime,json
from django.http import HttpResponse




class userSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    print(queryset)
    serializer_class = userSerializers


# Create your views here.
def index(request):
    productList=Products.objects.all()[:20]
    categoryList = Category.objects.annotate(num_category=Count('products'))[:6]
    context = {
        'productList': productList,
        'categoryList':categoryList
    }
    return render(request, "index.html",context)

def shop(request):
    productList=Products.objects.all()
    categoryList=Category.objects.annotate(num_category=Count('products'))


    context = {
        'productList': productList,
        'categoryList':categoryList
    }
    return render(request, "category.html",context)


def detaiPage(request,product_id):
    productDetail=Products.objects.filter(id=product_id).values()
    cat=Category.objects.filter(id=productDetail[0]['category_id_id'])
    productList=Products.objects.filter(category_id_id=productDetail[0]['category_id_id'])
    context = {
        'productDetail': productDetail[0],
        'cat':cat[0],
        'productList':productList
    }
    return render(request, "single-product.html",context)

def categoryPage(request,category_id):
    productDetail=Products.objects.filter(category_id_id=category_id).all()
    categoryList = Category.objects.annotate(num_category=Count('products'))
    context = {
        'productList': productDetail,
        'categoryList': categoryList
    }
    return render(request, "category.html", context)

def login(request):
    return render(request, "login.html")

def loadUserRegistration(request):
    return render(request, "registration.html")

def addUser(request):
    if request.method=='POST':
        firstName=request.POST['firstName']
        lastName=request.POST['lastName']
        password=request.POST['password']
        email=request.POST['email']
        m_number=request.POST['mobileNumber']
        altNumber=request.POST['altNumber']
        user = Users(firstName=firstName,email=email, lastName=lastName, mobileNumber=m_number,alternateNumber=altNumber)
        login=Login(email=email,password=password,login_user_id=user)
        user.save()
        login.save()
        return redirect('/login')

def validateUser(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=Login.objects.filter(email=email).first()
        if not user or not user.password==password:
            return redirect('/login')
        else:
            request.session['email']=email
            request.session['login_id']=user.id
            request.session['is_loged_in']=jwt.encode({
                    'public_id': email,
                    'exp': datetime.datetime.utcnow().utcnow() + datetime.timedelta(minutes=60)
                }, 'krunaldavara')
            return redirect('/')


def logout(request):
    if request.session:
        request.session.clear()
        return redirect('/')

@login_required
def addToCart(request):
    product=Products.objects.filter(id=request.POST['product_id']).first()
    user = Login.objects.filter(id=request.session['login_id']).first()
    if int(product.quantity)>=int(request.POST['quantity']):
        cart=Cart(product=product,user=user, quantity=request.POST['quantity'])
        cart.save()
        cart_count = Cart.objects.filter(user_id=request.session['login_id']).count()
        return HttpResponse(json.dumps({'cart_count': cart_count}), content_type="application/json")
    else:
        return {'status':'no'}

@login_required
def loadCart(request):
    cartList=Cart.objects.filter(user_id=request.session['login_id']).all().select_related()

    dataList={}
    for data in cartList:
        productList=Products.objects.filter(id=data.product_id).first()
        dataList[data.id]=[data,productList]

    context = {
        'dataList':dataList
    }
    return render(request, "cart.html", context)

@login_required
def deleteCart(request,cart_id):
    cart = Cart.objects.filter(id=cart_id).first()
    cart.delete()
    return redirect('loadCart')