import razorpay
from django.shortcuts import render, redirect
from .models import userInfo, User, Station, Bike, Employee, contactUS, Rent, Payment, userProof
from .forms import userForm, userInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from .filters import bike_filter
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.template.loader import get_template


def GeneratePDF(request):
    user = request.GET.get('Tid')
    obj = Payment.objects.get(Transaction_id=user)
    objT = obj.Transaction_id
    print(obj)
    context = {"Pay_user": obj, "today": "today", "Transaction": objT}

    return render(request, 'bike/invoice.html', context)


def History(request):
    user = request.user.username
    obj = Payment.objects.filter(Payment_user=user)
    print(obj)

    context = {
        "Pay_user": obj,
        "today": "today",
    }
    return render(request, 'user/history.html', context)


def home(request):
    stations = Station.objects.all()
    bikes = Bike.objects.filter(bike_available="Available")
    bikes_filter = bike_filter(request.GET, queryset=bikes)
    context = {'stations': stations, 'bikes': bikes, 'filter': bikes_filter}
    return render(request, 'home.html', context)


def register_user(request):

    if request.method == 'POST':
        user_form = userForm(request.POST)
        user_info_form = userInfoForm(request.POST, request.FILES)
        
        if user_form.is_valid() and user_info_form.is_valid():

            user_Proof = request.POST.get('user_Proof')
            proof_of_user = request.POST.get('proof_of_user')
            
            proofs = userProof.objects.all()
            
            has_valid=False
           
            if user_Proof == "Aadhaar Card":
                
                for proof in proofs:
                    if proof.Adhar_card == proof_of_user:
                        has_valid=True

            elif user_Proof == "Driving Licence":
                for proof in proofs:
                    if proof.driving_licence  == proof_of_user:
                        has_valid=True
            else:
                for proof in proofs:
                    if proof.passport_No  == proof_of_user:
                        has_valid=True

            if has_valid==True:
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                user_info = user_info_form.save(commit=False)
                user_info.user = user
                user_info.save()

                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(username=username, password=password)

                if user:
                    login(request, user)
            else:
                context={"msg":"proof of user is not valid"}
                return render(request, 'user/register.html', context)
            
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
    bikes = Bike.objects.filter(bike_available="Available")
    bikes_filter = bike_filter(request.GET, queryset=bikes)
    bikes_rents = []
    for i in bikes_filter.qs:
        current_bike_rent = Rent.objects.get(bike_rent=i.bike_number)
        bikes_rents.append(current_bike_rent)
    fin_ans = zip(bikes_rents, bikes_filter.qs)
    fin_ans = list(fin_ans)
    context = {'stations': stations, 'bikes': bikes,
               'filter': bikes_filter, 'bikes_rents': bikes_rents, 'fin_ans': fin_ans}

    return render(request, 'bike/take_bike.html', context)


@login_required(login_url='error')
def return_bike(request):
    current_user = request.user
    current_user_info = userInfo.objects.get(user_id=current_user.id)
    flag = True
    try:
        current_bike = Bike.objects.get(
            bike_number=current_user_info.user_bike)
        context = {'current_bike': current_bike, 'flag': flag}
    except:
        flag = False
        context = {'flag': flag}

    if request.method == "POST":
        superkey = request.POST.get("emp_superkey")
        try:
            check = Employee.objects.get(employee_superkey=superkey)
            current_user = userInfo.objects.get(user_id=request.user.id)
            bike_number = current_user.user_bike
            payment_obj = Payment.objects.get(Payment_bike_number=bike_number)
            payment_obj.Payment_emp_name = check.employee_name
            payment_obj.save()
            current_user.user_bike = "NOT TAKEN"
            current_user.save()
            current_bike = Bike.objects.get(bike_number=bike_number)
            current_bike.bike_available = "Available"
            current_bike.bike_user = "NONE"
            current_bike.save()
            return redirect('success_return')
        except:
            context = {'current_bike': current_bike,
                       'flag': True, 'error_flag': True, 'error': "Superkey is Invalid"}

    return render(request, 'bike/return_bike.html', context)


def payment(request):

    if request.method == "POST":
        name = request.POST.get('name')
        amount = request.POST.get('amount')

        client = razorpay.Client(
            auth=("rzp_test_pQD1ejHNOtqS0Y", "pqikXx7KeWw8Vv03XElgJKtJ"))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})

        selected_bike_number = request.GET.get('selected_bike')
        bike_rent_number = request.GET.get('bike_rent_number')
        bike_rent = request.GET.get('rent_select')
        selected_bike = Bike.objects.get(bike_number=selected_bike_number)
        selected_bike.bike_available = "Not Available"
        selected_bike.bike_user = request.user.username
        selected_bike.bike_rent_number = bike_rent_number
        selected_bike.bike_rent = bike_rent
        selected_bike.date_time = datetime.now()
        selected_bike.save()
        current_user = userInfo.objects.get(user_id=request.user.id)
        current_user.user_bike = selected_bike_number
        current_user.save()

        payment_obj = Payment()
        payment_obj.Payment_user = request.user.username
        payment_obj.Payment_station = selected_bike.bike_station
        payment_obj.Payment_bike_number = selected_bike_number
        payment_obj.Payment_bike_color = selected_bike.bike_color
        payment_obj.Payment_bike_type = selected_bike.bike_type
        payment_obj.Payment_bike_model = selected_bike.bike_model
        payment_obj.Payment_bike_brand = selected_bike.bike_brand
        payment_obj.Payment_rent_type = bike_rent
        payment_obj.Payment_rent_number = bike_rent_number
        payment_obj.Payment_bill_amount = amount
        payment_obj.save()

        return redirect('success_take')

    bike_rent_number = request.GET.get('bike_rent_number')
    bike_rent = request.GET.get('rent_select')
    selected_bike_number = request.GET.get('selected_bike')
    selected_bike = Bike.objects.get(bike_number=selected_bike_number)
    rented_BIke = Rent.objects.filter(bike_rent=selected_bike_number).first()

    context = {'selected_bike': selected_bike,
               'bike_rent_number': bike_rent_number, 'bike_rent': bike_rent, 'rented_BIke': rented_BIke}

    return render(request, 'bike/payment.html', context)


def error(request):
    return render(request, 'error.html')


@csrf_exempt
def success_take(request):
    return render(request, "bike/success_take.html")


def success_return(request):
    return render(request, "bike/success_return.html")


def contact(request):
    if request.method == 'POST':
        form = contactUS()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        form.name = name
        form.mail = email
        form.message = message
        form.save()
        return redirect('home')
    return render(request, 'contact.html')


def admin(request):
    return render(request, 'admin.html')


def profile(request):
    return render(request, 'user/profile.html')
