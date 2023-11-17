from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
from .models import Currency_rate
from _decimal import Decimal
from datetime import datetime
import pytz
import requests

from internet_project import settings


# Create your views here.hghghg

def index2(request):
    # Fetch data for Bitcoin (BTC)
    btc_data = get_crypto_data("btc-bitcoin")
    return print_crypto_info(btc_data)


def get_crypto_data(symbol):
    url = f"https://api.coinpaprika.com/v1/tickers/{symbol}"
    response = requests.get(url)
    data = response.json()
    return data


def print_crypto_info(data):
    response = HttpResponse()
    response.write("Name:" + data["name"])
    response.write("Symbol:" + data["symbol"])
    response.write("Price:" + f"${data['quotes']['USD']['price']}")
    response.write("1h %:" + f"{data['quotes']['USD']['percent_change_1h']}%")
    response.write("24h %:" + f"{data['quotes']['USD']['percent_change_24h']}%")
    response.write("7d %:" + f"{data['quotes']['USD']['percent_change_7d']}%")
    response.write("Market Cap:" + f"${data['quotes']['USD']['market_cap']}")
    response.write("Volume (24h):" + f"${data['quotes']['USD']['volume_24h']}")
    response.write("Circulating Supply:" + f"{data['circulating_supply']} {data['symbol']}")
    response.write("Last 7 Days:" + f"{data['quotes']['USD']['percent_change_7d']}%")
    return response


# Create your views here.
def index(request):
    fxTableData = [
        {'id': 1, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000, 'sevenDayPer': 50000,
         'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 2, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000, 'sevenDayPer': 50000,
         'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 3, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 4, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 4, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 5, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 6, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 7, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},

    ]
    for rowData in fxTableData:
        # Add a 'change_color' attribute to each entry based on the value of 'change_24h'
        rowData['changeStatus'] = 'positiveChange' if rowData['oneHrPer'] > 0 else 'negativeChange'
        rowData['changeStatus'] = 'positiveChange' if rowData['twoHrPer'] > 0 else 'negativeChange'
        rowData['changeStatus'] = 'positiveChange' if rowData['sevenDayPer'] > 0 else 'negativeChange'

    return render(request, 'internetProject/index.html', {'fxTableData': fxTableData})


def home(request):
    return render(request, "internetProject/index.html")


def force_byte(pk):
    pass


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Passwords didn't match")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()

        messages.success(request,
                         "Your account has been successfully created.We have sent you a confirmation email, please confirm your email in order to activate your account  ")

        # Welcome Email

        subject = "Welcome to my App"
        message = "Hello" + myuser.first_name + "!! \n" + "Welcome to my App!! \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address to activate your account. \n\n Thanking you\n "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list)

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Internet Project"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)

        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],

        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "internetProject/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "internetProject/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')
    return render(request, "internetProject/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')


def currency(request, from_currency, to_currency):
    return render(request, 'currency.html', {'from_currency': from_currency, 'to_currency': to_currency})



def index_jk(request):
    return render(request, "index_jk.html")


def payment(request):
    return render(request, "templates/payment.html")
