from django.shortcuts import render, redirect
from .models import userInfo, User, Station, Bike
from .forms import userForm, userInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from .filters import bike_filter
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum

MERCHANT_KEY = 'bKMfNxPPf_QdZppa'

# Create your views here.


def home(request):
    stations = Station.objects.all()
    bikes = Bike.objects.all()
    bikes_filter = bike_filter(request.GET, queryset=bikes)
    context = {'stations': stations, 'bikes': bikes, 'filter': bikes_filter}
    return render(request, 'home.html', context)


def register_user(request):

    if request.method == 'POST':
        user_form = userForm(request.POST)
        user_info_form = userInfoForm(request.POST, request.FILES)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()

            return redirect('home')

        else:
            context = {'user_form.errors': user_form.errors,
                       'user_info_form.errors': user_info_form.errors}
            return render(request, 'user/register.html', context)
    else:

        user_form = userForm()
        user_info_form = userInfoForm()

        context = {'user_form': user_form,
                   'user_info_form': user_info_form}

        return render(request, 'user/register.html', context)


def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or password is not valid!')
            return redirect('login_user')

    return render(request, 'user/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='error')
def take_bike(request):
    stations = Station.objects.all()
    bikes = Bike.objects.all()
    bikes_filter = bike_filter(request.GET, queryset=bikes)
    context = {'stations': stations, 'bikes': bikes, 'filter': bikes_filter}
    if request.method=='POST':
        param_dict={

            'MID': 'DIY12386817555501617',
            'ORDER_ID': 'order.order_id', #put order id in string here
            'TXN_AMOUNT': '1', #put amount here in string
            'CUST_ID': 'email', #put customer id here
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/user/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return  render(request, 'user/paytm.html', {'param_dict': param_dict})


    return render(request, 'bike/take_bike.html', context)


def return_bike(request):
    return render(request, 'bike/return_bike.html')


def error(request):
    return render(request, 'error.html')

@csrf_exempt
def handleRequest(request):
     # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'user/paymentstatus.html', {'response': response_dict})