
from django.shortcuts import render, redirect,HttpResponse
from .models import Product,Customer,Cart,OrderPlaced
from django.contrib.auth.models import User
from django.contrib import messages  # import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

def home(request):
   
    top_wears = Product.objects.filter(category="TW")
    bottom_wear = Product.objects.filter(category="BW")
    mobile = Product.objects.filter(category="M")
    laptop = Product.objects.filter(category="L")

    total_cart = 0
     
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))


    products_dic = {"top_wears": top_wears, "mobile": mobile,
                    "bottom_wear": bottom_wear, "laptop": laptop,"total_cart":total_cart}
    return render(request, 'app/home.html', products_dic)

@login_required(login_url='/login')
def product_detail(request, cat_id):
    total_cart = 0
     
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))

    product = Product.objects.get(id=cat_id)

    is_item_present = False

    is_item_present = Cart.objects.filter(  Q(product=product.id) & Q(user=request.user)  )


    products_dic = {"product": product,"is_item_present":is_item_present,"total_cart":total_cart}
    return render(request, 'app/productdetail.html', products_dic)


@login_required(login_url='/login')
def cart(request):

    
    user = request.user
    product_id = request.GET.get("product_id")
    product = Product.objects.get(id=product_id)
    Mycart = Cart(user=user,product=product)
    Mycart.save()

    return redirect("/showcart")

@login_required(login_url='/login')
def showcart(request):

    total_cart = 0
     

        
    if request.user.is_authenticated:
        user = request.user
        allcarts = Cart.objects.filter(user=user).order_by('-date')
        total_cart = len(Cart.objects.filter(user=request.user))
       
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if(cart_product):
            for p in cart_product:
                tempamount =(p.quantity * p.product.discount)
                amount += tempamount
              



            cartDic = {"allcart":allcarts,"amount":amount,"totalamount": amount + shipping_amount,"total_cart":total_cart}
        else:
           return render(request, 'app/emptyCart.html')

    

    return render(request, 'app/showcart.html',cartDic)


@login_required(login_url='/login')
def pluscart(request):
    if request.method =="GET":
        pro_id =request.GET['pro_id']
       
        c = Cart.objects.get( Q(product=pro_id)  & Q(user=request.user)  )
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        if(cart_product):
            for p in cart_product:
                tempamount =(p.quantity * p.product.discount)
                amount += tempamount
               
    
            data={
                "quantity":c.quantity,
                "amount":amount,
                "totalamount":amount + shipping_amount
            }
            return JsonResponse(data)



@login_required(login_url='/login')
def minuscart(request):
    if request.method =="GET":
        pro_id =request.GET['pro_id']
       
        c = Cart.objects.get( Q(product=pro_id)  & Q(user=request.user)  )
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        if(cart_product):
            for p in cart_product:
                tempamount =(p.quantity * p.product.discount)
                amount += tempamount
                
            data={
                "quantity":c.quantity,
                "amount":amount,
                "totalamount":amount + shipping_amount
    
            }
            return JsonResponse(data)


@login_required(login_url='/login')
def removecart(request):
    if request.method =="GET":
        pro_id =request.GET['pro_id']
       
        c = Cart.objects.get( Q(product=pro_id)  & Q(user=request.user)  )
       
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        if(cart_product):
            for p in cart_product:
                tempamount =(p.quantity * p.product.discount)
                amount += tempamount
                totalamount = amount + shipping_amount
    
            data={
                
                "amount":amount,
                "totalamount":totalamount
            }
            return JsonResponse(data)




@login_required(login_url='/login')
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required(login_url='/login')
def profile(request):
    
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        user = request.user
        costumer = Customer(user=user,name=name,address=address,address2=address2,city=city,zipcode=zip,state=state)
        costumer.save()
        messages.success(request, "Address is been added successfully")
        user_dic= {"user":user}
    total_cart = 0
     
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))


    return render(request, 'app/profile.html',{"total_cart":total_cart})

@login_required(login_url='/login')
def address(request):
    total_cart=0
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))
    address = Customer.objects.filter(user=request.user)
    addres_di= {'address':address,"total_cart":total_cart}

    return render(request, 'app/address.html',addres_di)

@login_required(login_url='/login')
def orders(request):
    total_cart=0
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))
    allOrders = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')

    return render(request, 'app/orders.html',{"orders":allOrders,"total_cart":total_cart})


def category(request, cat):
    total_cart=0
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))
    category = Product.objects.filter(category=cat)
    cat_dic = {"category": category,"total_cart":total_cart}
    return render(request, 'app/category.html', cat_dic)


def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']
   
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            # Redirect to a success page.
            messages.success(request, "Login completed")
            return redirect("/")

        else:
            # No backend authenticated the credentials
            messages.warning(request, "Credentials didn't matched")
    return render(request, 'app/login.html')


def customerregistration(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        cpassword = request.POST['cpass']
        if(len(password) > 6):
            if(password == cpassword):
                if(User.objects.filter(username=username).exists()):
                    messages.warning(request, "Username already exists")
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    messages.success(request, "Registration completed")

            else:
                messages.warning(
                    request, "Password and Confirm Password are not matched")
        else:
            messages.warning(request, "Password must be more than six chars")

    return render(request, 'app/customerregistration.html')

@login_required(login_url='/login')
def checkout(request):
      allcarts = Cart.objects.filter(user=request.user)
      alladress = Customer.objects.filter(user=request.user)
       
     
      amount = 0.0
      shipping_amount = 70.0
      total_amount = 0.0

      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      total_cart=0
      if request.user.is_authenticated:
          total_cart = len(Cart.objects.filter(user=request.user))
      if(cart_product):
            for p in cart_product:
                tempamount =(p.quantity * p.product.discount)
                amount += tempamount
            totalamount = amount + shipping_amount

      shopingDetailDic ={"carts":allcarts,"address":alladress,"amount":totalamount,"total_cart":total_cart}
       
      return render(request, 'app/checkout.html',shopingDetailDic,)


@login_required(login_url='/login')
def paymentdone(request):
    user = request.user
    customerId = request.GET.get("custadd")
    costumer = Customer.objects.get(id=customerId)
    carts = Cart.objects.filter(user=user)

    for c in carts:
        OrderPlaced(user=user,costumer=costumer,product=c.product,quantity=c.quantity).save()
        c.delete()

    return redirect("/orders")


def logOut(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("/")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/changepassword.html', {
        'form': form
    })



def search(request):
    
    search_text = request.GET["search"]
    searchQuery = Product.objects.filter( Q(title__icontains=search_text) |  Q(brand__icontains=search_text))  
    total_cart=0
    if request.user.is_authenticated:
        total_cart = len(Cart.objects.filter(user=request.user))
    return render(request,"app/search.html",{"search":searchQuery,"qrr":search_text,"total_cart":total_cart})