from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as dj_logout, login as dj_login
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


from .models import Product
from .models import ProductCategory
from .models import Profile
from .models import Opg


def index(request):
    return render(request, "OPG_app/index.html",{"welcome": _("Welcome to agricultural application!"), "nav":False})

def products(request):
    if not request.user.is_authenticated:
        return render(request, "OPG_app/index.html", {"message": _("You are not logged in. Please login!"), "nav":False})

    context = {
        # "products": Product.objects.filter(opg_id=request.user.profile.opg_id).all(),
        "products": Product.objects.all(),
        "nav": True,
    }

    return render(request, "OPG_app/products.html", context)



def product(request, product_id):
    if not request.user.is_authenticated:
        return render(request, "OPG_app/index.html", {"message": _("You are not logged in. Please login!"), "nav":False})
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404(_("Product does not exist!"))
    context = {
        "product": product,
        "categories": ProductCategory.objects.all().distinct('name'),
        "message": "Editing Product",
        "nav": True,
    }
    return render(request, "OPG_app/product.html", context)



def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        opg_name = request.POST.get("opg_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username != email:
            return render(request, "OPG_app/register.html",
                          {"message": _("Registration did not succeed due to input error, please repeat input!")})
        try:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password, email=email)
            profile = Profile(address=address, phone=phone, user=user)
            opg_list = Opg.objects.filter(name=opg_name)
            if len(opg_list) == 0:
                opg = Opg(name=opg_name)
                opg.save()
            else:
                opg = Opg.objects.filter(name=opg_name).first()
            user.save()
            profile.save()
            Profile.objects.filter(pk=profile.id).update(opg_id=opg)
            return HttpResponseRedirect(reverse("login"))
        except:
            return render(request, "OPG_app/register.html",
                          {"message": _("Registration did not succeed due to input error, please repeat input!")})

    else:
        return render(request, "OPG_app/register.html", {"message": _("Registration of new user and agricultural subject")})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj_login(request, user)
            return HttpResponseRedirect(reverse("products"))
        else:
            return render(request, "OPG_app/login.html", {'form': form, "message": _("Login did not succeed due to input error, please repeat input!")})
    else:
        form = AuthenticationForm()
    return render(request, 'OPG_app/login.html', {'form': form})



def logout(request):
    dj_logout(request)
    form = AuthenticationForm()
    return render(request, "OPG_app/login.html", {'form': form})


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get("product")
        if name != '':
            category_id = request.POST.get("product_category")
            category = ProductCategory.objects.filter(id=category_id).first()
            product = Product(name=name,category=category)
            product.save()
            return HttpResponseRedirect(reverse("products"))
        else:
            raise Http404(_("Please enter the name of the product you want to create!"))
    else:
        context = {
            "message": "Create Product",
            "categories": ProductCategory.objects.all().distinct('name'),
            "nav": True,
        }
        return render(request, "OPG_app/add_product.html",context)


@login_required
def edit_product(request, product_id):
    if request.method == 'POST':
        name = request.POST.get("product")
        category = request.POST.get("product_category")
        if name != '':
            Product.objects.filter(pk=product_id).update(name=name,category=category)
        else:
            Product.objects.filter(pk=product_id).update(category=category)
        return HttpResponseRedirect(reverse("products"))
    else:
        return HttpResponseRedirect(reverse("product", args=(product_id,)))


def del_product(request, product_id):
    if not request.user.is_authenticated:
        return render(request, "OPG_app/index.html", {"message": _("You are not logged in. Please login!"), "nav":False})
    if request.method == 'GET':
        try:
            Product.objects.get(pk=product_id).delete()
        except:
            print('Product does not exist!')
        return HttpResponseRedirect(reverse("products"))

def profile(request):
    if not request.user.is_authenticated:
        form = AuthenticationForm()
        return render(request, "OPG_app/login.html", {"message": _("You are not logged in. Please login!"), 'form':form})

    context = {
        "user": request.user.profile,
        "message": "View Profile",
        "nav": True,

    }
    return render(request, "OPG_app/profile.html", context)

def edit_profile(request):
    if not request.user.is_authenticated:
        form = AuthenticationForm()
        return render(request, "OPG_app/login.html", {"message": _("You are not logged in. Please login!"), 'form':form})

    if request.method == 'POST':

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        opg_id = request.POST.get("opg_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        updated_profile = request.user.profile.id
        updated_user = request.user.id
        if opg_id != '':
            Profile.objects.filter(pk=updated_profile).update(opg_id=opg_id)
        if address != '':
            Profile.objects.filter(pk=updated_profile).update(address=address)
        if phone != '':
            Profile.objects.filter(pk=updated_profile).update(phone=phone)

        if first_name != '':
            User.objects.filter(pk=updated_user).update(first_name=first_name)
        if last_name != '':
            User.objects.filter(pk=updated_user).update(last_name=last_name)
        return HttpResponseRedirect(reverse("profile"))

    context = {
        "user": request.user.profile,
        "user_basic": request.user,
        "users": Profile.objects.all().distinct('opg_id'),
        "message": "Edit Profile",
        "nav": True,
    }
    return render(request, "OPG_app/edit_profile.html", context)
