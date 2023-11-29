import os

import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic import TemplateView
from internet_project.settings import REQUESTS_CA_BUNDLE
from .models import Complaint, Feedback, Currency_rate
from .forms import ComplaintForm, Feedback
from .tokens import generate_token
from .models import Currency_rate, CryptoData, CoinDetail, CryptoStateData, Payment, UserProfile
from _decimal import Decimal
from datetime import datetime, timedelta
from math import copysign
# import pytz
import json
import certifi
# import pytz
import requests
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import reverse_lazy, reverse
import pytz
# import requests
from django.utils import timezone

from internet_project import settings

duration = 15
@login_required()
def user_profile(request):
    # Assuming the user is logged in
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    context = {
        'user': user,
        'user_profile': user_profile,
    }

    return render(request, 'internetProject/user_profile.html', context)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'internetProject/password_reset_form.html'
    email_template_name = 'internetProject/password_reset_email.html'
    subject_template_name = 'internetProject/password_reset_email_subject.txt'
    success_url = '/password_reset/done/'
    # def form_valid(self, form):
    #     # your form processing logic here
    #
    #     # manually construct the success URL
    #     success_url = self.request.build_absolute_uri(reverse('internetProject:password_reset'))
    #
    #     # perform any additional logic if needed
    #
    #     return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'internetProject/password_reset_done.html'


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'internetProject/password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'internetProject/password_reset_confirm.html'
    success_url = '/password_reset_complete/'

    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')

        if uidb64 is not None and token is not None:
            context = {'uidb64': uidb64, 'token': token}
            return self.render_to_response(context)
        else:
            return HttpResponse("Invalid reset link")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs.get('uidb64', '')
        context['token'] = self.kwargs.get('token', '')
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'internetProject/password_reset_complete.html'


def index(request):
    default_limit = 10
    limit = default_limit

    page = request.GET.get('page', 1)
    search = request.GET.get('search', '')
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    offset = (page - 1) * limit

    crypto_data_query = CryptoData.objects.filter(limit=limit, offset=offset, search=search)

    if crypto_data_query.exists():
        crypto_data_entry = crypto_data_query.first()
        coins_data = crypto_data_entry.data
        total_items = crypto_data_entry.total_items

        if timezone.now() - crypto_data_entry.last_updated > timezone.timedelta(minutes=duration):
            api_data = get_crypto_data(limit, offset, search)
            crypto_data_entry.data = api_data['data']['coins']
            crypto_data_entry.total_items = api_data['data']['stats']['total']
            crypto_data_entry.last_updated = timezone.now()
            crypto_data_entry.save()
            total_items = api_data['data']['stats']['total']
            coins_data = api_data['data']['coins']

    else:
        api_data = get_crypto_data(limit, offset, search)
        crypto_data = api_data['data']['coins']
        total_items = api_data['data']['stats']['total']
        coins_data = api_data['data']['coins']
        CryptoData.objects.create(total_items=api_data['data']['stats']['total'], last_updated=timezone.now(),
                                  limit=limit, offset=offset, data=crypto_data, search=search)

    total_pages = (total_items + limit - 1) // limit

    row_index = (page - 1) * limit + 1
    for rowData in coins_data:
        print(rowData['change'])
        check_decimal = 0
        if rowData['change'] is not None:
            check_decimal = Decimal(str(rowData['change']))
        sign = copysign(1, check_decimal)
        rowData['changeStatus'] = 'green' if sign > 0 else 'red'
        rowData['index'] = row_index
        row_index = row_index + 1
        timestamp = int(rowData['listedAt'])
        rowData['listedAt'] = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    top_ranked = get_top_data("ranking")
    for rowData in top_ranked:
        check_decimal = Decimal(str(rowData['change']))
        sign = copysign(1, check_decimal)
        rowData['changeStatus'] = 'green' if sign > 0 else 'red'
        float_array = [float(x) if x is not None else None for x in rowData['sparkline']]
        rowData['sparkline'] = json.dumps(float_array)

    top_changed = get_top_data("changed")
    for rowData in top_changed:
        check_decimal = Decimal(str(rowData['change']))
        sign = copysign(1, check_decimal)
        rowData['changeStatus'] = 'green' if sign > 0 else 'red'
        float_array = [float(x) if x is not None else None for x in rowData['sparkline']]
        rowData['sparkline'] = json.dumps(float_array)

    top_priced = get_top_data("priced")
    for rowData in top_priced:
        check_decimal = Decimal(str(rowData['change']))
        sign = copysign(1, check_decimal)
        rowData['changeStatus'] = 'green' if sign > 0 else 'red'
        float_array = [float(x) if x is not None else None for x in rowData['sparkline']]
        rowData['sparkline'] = json.dumps(float_array)

    return render(request, 'internetProject/index.html',
                  {'cryptocurrencies': coins_data, 'page': page, 'total_pages': total_pages, 'top_ranked': top_ranked,
                   'top_changed': top_changed, 'top_priced': top_priced, 'search': search})


def coin_details(request, coin_id, from_currency, to_currency):
    coin_data = get_coin_details(coin_id)
    currencys = {'USD', 'EUR', 'JPY', 'CAD', 'CNY'}
    data, latest_rate = get_currency_rate(request, from_currency, to_currency)
    print(data)
    return render(request, 'internetProject/coin_details.html',
                  {'coin_id': coin_id, 'coin_data': coin_data, 'data': data, 'latest_rate': latest_rate,
                   'from_currency': from_currency,
                   'to_currency': to_currency, 'currencys': currencys})


def get_crypto_data(limit, offset, search):
    url = f"https://api.coinranking.com/v2/coins?limit={limit}&timePeriod=3h&offset={offset}&search={search}"
    response = requests.get(url)
    data = response.json()
    return data


def get_coin_details(coin_id):
    # Check if data exists in the database
    try:
        coin_detail = CoinDetail.objects.get(coin_id=coin_id)
        if coin_detail.last_updated > timezone.now() - timedelta(minutes=duration):
            return coin_detail
    except CoinDetail.DoesNotExist:
        pass  # Continue to fetch data from the API

    url = f"https://api.coinranking.com/v2/coin/{coin_id}"
    response = requests.get(url)
    api_data = response.json()
    coin_data = api_data['data']['coin']

    coin_detail, created = CoinDetail.objects.update_or_create(
        coin_id=coin_id,
        defaults={
            'name': coin_data['name'],
            'symbol': coin_data['symbol'],
            'description': coin_data['description'],
            'icon_url': coin_data['iconUrl'],
            'tier': coin_data['tier'],
            'rank': coin_data['rank'],
            'price': coin_data['price'],
            'btc_price': coin_data['btcPrice'],
            'price_at': datetime.utcfromtimestamp(int(coin_data['priceAt'])).strftime('%Y-%m-%d %H:%M:%S'),
            'number_of_markets': coin_data['numberOfMarkets'],
            'number_of_exchanges': coin_data['numberOfExchanges'],
            'volume_24h': coin_data['24hVolume'],
            'market_cap': coin_data['marketCap'],
            'fully_diluted_market_cap': coin_data['fullyDilutedMarketCap'],
            'change': coin_data['change'],
            'all_time_high_price': coin_data['allTimeHigh']['price'],
            'all_time_high_timestamp': datetime.utcfromtimestamp(int(coin_data['allTimeHigh']['timestamp'])).strftime(
                '%Y-%m-%d %H:%M:%S'),
            'website_url': coin_data['websiteUrl'],
            'last_updated': timezone.now(),
        }
    )

    return coin_detail


def get_top_data(type):
    if type == "changed":
        url = f"https://api.coinranking.com/v2/coins?limit=3&orderBy=change"
    elif type == "priced":
        url = f"https://api.coinranking.com/v2/coins?limit=3&orderBy=price"
    else:
        url = f"https://api.coinranking.com/v2/coins?limit=3"
    crypto_data_query = CryptoStateData.objects.filter(type=type)
    if crypto_data_query.exists():
        crypto_data_entry = crypto_data_query.first()
        if timezone.now() - crypto_data_entry.last_updated > timezone.timedelta(minutes=duration):
            response = requests.get(url)
            api_data = response.json()
            crypto_data_entry.data = api_data['data']['coins']
            crypto_data_entry.last_updated = timezone.now()
            crypto_data_entry.save()
    else:
        response = requests.get(url)
        api_data = response.json()
        crypto_data_entry = api_data['data']['coins']
        CryptoStateData.objects.create(type=type, last_updated=timezone.now(), data=crypto_data_entry)
    return crypto_data_entry.data


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
def index2(request):
    fxTableData = [
        {'id': 1, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': -50000,
         'twoHrPer': -50000, 'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5,
         'Circulating_Supply': 5},
        {'id': 2, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': 50000,
         'twoHrPer': 50000, 'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5,
         'Circulating_Supply': 5},
        {'id': 3, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': -50000,
         'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 4, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': -50000,
         'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 4, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': 50000,
         'twoHrPer': -50000,
         'sevenDayPer': -50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 5, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': 50000,
         'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 6, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': -50000,
         'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 7, 'Name': 'Bitcoin', 'logo': 'https://shorturl.at/kmoqL', 'Price': 50000, 'oneHrPer': -50000,
         'twoHrPer': 50000,
         'sevenDayPer': -50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},

    ]
    for rowData in fxTableData:
        # Add a 'change_color' attribute to each entry based on the value of 'change_24h'
        rowData['change1Status'] = 'positiveChange' if rowData['oneHrPer'] > 0 else 'negativeChange'
        rowData['change2Status'] = 'positiveChange' if rowData['twoHrPer'] > 0 else 'negativeChange'
        rowData['change7Status'] = 'positiveChange' if rowData['sevenDayPer'] > 0 else 'negativeChange'

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
            return HttpResponseRedirect(reverse('internetProject:signup'))

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return HttpResponseRedirect(reverse('internetProject:signup'))

        if len(username) > 10:
            messages.error(request, "Passwords didn't match")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')

        # Create a User instance
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True

        # Save the User instance
        myuser.save()

        # Create a UserProfile instance and link it to the User
        user_profile = UserProfile(user=myuser)
        id_proof = request.FILES.get('id_proof')

        if id_proof:
            # Validate file format (optional)
            if not id_proof.name.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
                messages.error(request, "Invalid ID proof format. Please upload a valid image (jpg, jpeg, png) or PDF.")
                return redirect('home')

            # Specify the subfolder within MEDIA_ROOT to store ID proofs
            id_proof_subfolder = 'id_proofs'

            # Construct the path to the subfolder
            id_proof_path = os.path.join(settings.MEDIA_ROOT, id_proof_subfolder, id_proof.name)

            # Create the subfolder if it doesn't exist
            os.makedirs(os.path.dirname(id_proof_path), exist_ok=True)

            # Save the ID proof file to the specified subfolder
            with open(id_proof_path, 'wb') as destination:
                for chunk in id_proof.chunks():
                    destination.write(chunk)

            # Save the ID proof path to the UserProfile model
            user_profile.id_proof_path = id_proof_path

        # Save the UserProfile instance
        user_profile.save()

        messages.success(request,
                         "Your account has been successfully created. We have sent you a confirmation email, please confirm your email to activate your account.")

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

        # return redirect('internetProject/signin')
        return redirect('internetProject:signin')
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('internetProject:index'))
    return render(request, "internetProject/signup.html")


# def signup(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
#
#         if User.objects.filter(username=username):
#             messages.error(request, "Username already exists! Please try some other username")
#             return redirect('home')
#
#         if User.objects.filter(email=email):
#             messages.error(request, "Email already registered")
#             return redirect('home')
#
#         if len(username) > 10:
#             messages.error(request, "Passwords didn't match")
#
#         if pass1 != pass2:
#             messages.error(request, "Passwords didn't match!")
#
#         if not username.isalnum():
#             messages.error(request, "Username must be Alpha-Numeric!")
#             return redirect('home')
#
#
#
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.is_active = True
#
#         id_proof = request.FILES.get('id_proof')
#
#         if id_proof:
#             # Validate file format (optional)
#             if not id_proof.name.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
#                 messages.error(request, "Invalid ID proof format. Please upload a valid image (jpg, jpeg, png) or PDF.")
#                 return redirect('home')
#
#             # Save the ID proof file to MEDIA_ROOT
#             id_proof_path = os.path.join(settings.MEDIA_ROOT, id_proof.name)
#             with open(id_proof_path, 'wb') as destination:
#                 for chunk in id_proof.chunks():
#                     destination.write(chunk)
#
#             # Save the ID proof path to the user model or your database
#             myuser.id_proof_path = id_proof_path
#
#         myuser.save()
#
#         messages.success(request,
#                          "Your account has been successfully created.We have sent you a confirmation email, please confirm your email in order to activate your account  ")
#
#         # Welcome Email
#
#         subject = "Welcome to my App"
#         message = "Hello" + myuser.first_name + "!! \n" + "Welcome to my App!! \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address to activate your account. \n\n Thanking you\n "
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [myuser.email]
#         send_mail(subject, message, from_email, to_list)
#
#         # Email Address Confirmation Email
#
#         current_site = get_current_site(request)
#         email_subject = "Confirm your email @ Internet Project"
#         message2 = render_to_string('email_confirmation.html', {
#             'name': myuser.first_name,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': generate_token.make_token(myuser)
#
#         })
#         email = EmailMessage(
#             email_subject,
#             message2,
#             settings.EMAIL_HOST_USER,
#             [myuser.email],
#
#         )
#         email.fail_silently = True
#         email.send()
#
#         return redirect('internetProject/signin')
#
#     return render(request, "internetProject/signup.html")

#
# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
#
#         user = authenticate(username=username, password=pass1)
#
#         if user is not None:
#             login(request, user)
#             fname = user.first_name
#             return render(request, "internetProject/index.html", {'fname': fname})
#         else:
#             messages.error(request, "Bad Credentials")
#             return redirect('home')
#     return render(request, "internetProject/signin.html")

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('internetProject:index'))
    else:
        if request.method == 'POST':
            username = request.POST['username']
            pass1 = request.POST['pass1']

            user = authenticate(username=username, password=pass1)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('internetProject:index'))
            else:
                messages.error(request, "Bad Credentials")
                # return redirect('home')
    return render(request, "internetProject/signin.html")


def about_us(request):
    return render(request, "about-us.html")


def faq(request):
    return render(request, "faq.html")


def complaint_form(request):
    msg = ''
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'You exceeded the number of levels for this course.'
            return render(request, 'success.html', {'msg': msg})

            # Create a success page
    else:
        form = ComplaintForm()

    return render(request, 'complaint_form.html', {'form': form})


def feedback_form(request):
    msg = ''
    if request.method == 'POST':
        form = Feedback(request.POST)
        if form.is_valid():
            form.save()
            msg = 'You exceeded the number of levels for this course.'
            return render(request, 'success.html', {'msg': msg})

            # Create a success page
    else:
        form = Feedback()

    return render(request, 'feedback.html', {'form': form})


# def send_email(request):
#     subject = 'Testing mail'
#     from_email = 'internetproject99@email.com'
#     msg = '<p> Welcome to Our <b>Project </b></p>'
#     to = 'shreyanshdalwadi@gmail.com'
#     msg = EmailMultiAlternatives(subject, msg, from_email, [to])
#     msg.content_subtype = 'html'
#     msg.send()


def send_email(request):
    try:
        if request.method == 'POST':
            # Assuming your form has an input field named 'email'
            email_address = request.POST.get('email')

            subject = 'Testing mail'
            from_email = 'internetproject99@email.com'

            # Render the HTML content from the template
            html_content = render_to_string('your_template.html')

            # Create a text/plain version for clients that don't support HTML
            text_content = strip_tags(html_content)

            # Create the EmailMultiAlternatives object and attach both HTML and text versions
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email_address])
            msg.attach_alternative(html_content, "text/html")

            # Send the email
            msg.send()

            # Return a success response if needed
            return render(request, 'internetProject/index.html', {'message': 'Email sent successfully!'})
        else:
            # Handle the case when the form is not submitted
            return HttpResponse('Form not submitted.')
    except Exception as e:
        # Log the exception or handle it in an appropriate way
        print(f"An error occurred while sending the email: {e}")
        # Return an error response if needed
        return HttpResponse('Failed to send email.')


@login_required()
def signout(request):
    logout(request)
    # messages.success(request, "Logged Out Successfully!")
    return HttpResponseRedirect(reverse('internetProject:index'))


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
        return redirect('internetProject:index')
    else:
        return render(request, 'activation_failed.html')


@login_required
def currency_pay(request, coin_id, from_currency, to_currency):
    return render(request, 'currency_pay.html',
                  {'from_currency': from_currency, 'to_currency': to_currency, 'coin_id': coin_id})


def currency(request, from_currency, to_currency):
    currencys = {'USD', 'EUR', 'JPY', 'CAD', 'CNY'}
    data, latest_rate = get_currency_rate(request, from_currency, to_currency)
    print(data)
    return render(request, 'internetProject/coin_details.html',
                  {'data': data, 'latest_rate': latest_rate, 'from_currency': from_currency,
                   'to_currency': to_currency, 'currencys': currencys})


def get_currency_rate(request, from_currency, to_currency):
    api_key = settings.EXCHANGE_RATE_API_KEY
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'

    params = {
        'fsym': from_currency,
        'tsym': to_currency,
        'limit': 30,
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['Data']['Data']
        latest_rate = data[-1]
        for rate in data:
            timestamp = datetime.fromtimestamp(rate['time'])
            Currency_rate.objects.create(
                from_currency=from_currency,
                to_currency=to_currency,
                rate=rate['close'],
                time=timestamp,
            )
        data = json.dumps(data)
        return data, latest_rate
    else:
        return render(request, 'currency.html', {'error': "Error fetching data"})


def index_jk(request):
    return render(request, "index_jk.html")


# view for PayPal Payment Gateway Page
class PaymentView(TemplateView):
    # template_name = 'paymentPaypal.html'
    def get(self, request, from_currency, to_currency, *args, **kwargs):
        amount = request.GET.get('amount')
        if amount:
            data, latest_rate = get_currency_rate(request, from_currency, to_currency)
            total_price = Decimal(amount) * Decimal(latest_rate['close']).quantize(Decimal('0.00'))
            context = {
                'total_price': total_price,
            }
            print(context)
            return render(request, "paymentPaypal.html", context)
        else:
            return HttpResponse("Amount is required.", status=400)


@login_required
def payment(request):
    if request.method == 'POST':
        # Static PayPal JSON response
        # paypal_response = '''
        # {
        #     "id": "PAYPAL_TRANSACTION_ID",
        #     "intent": "CAPTURE",
        #     "status": "COMPLETED",
        #     "create_time": "2023-11-23T12:34:56Z",
        #     "update_time": "2023-11-23T12:35:00Z",
        #     "payer": {
        #         "name": {
        #             "given_name": "John",
        #             "surname": "Doe"
        #         },
        #         "email_address": "john.doe@example.com",
        #         "payer_id": "PAYPAL_PAYER_ID",
        #         "address": {
        #             "country_code": "US",
        #             "postal_code": "12345",
        #             "state": "CA",
        #             "city": "San Jose",
        #             "line1": "123 Main St"
        #         }
        #     },
        #     "purchase_units": [
        #         {
        #             "reference_id": "REFERENCE_ID",
        #             "amount": {
        #                 "value": "0.01",
        #                 "currency_code": "USD",
        #                 "breakdown": {
        #                     "item_total": {
        #                         "currency_code": "USD",
        #                         "value": "0.01"
        #                     }
        #                 }
        #             },
        #             "payee": {
        #                 "email_address": "merchant@example.com",
        #                 "merchant_id": "MERCHANT_ID"
        #             },
        #             "shipping": {
        #                 "address": {
        #                     "name": {
        #                         "full_name": "John Doe"
        #                     },
        #                     "address_line_1": "123 Main St",
        #                     "admin_area_1": "CA",
        #                     "admin_area_2": "San Jose",
        #                     "postal_code": "12345",
        #                     "country_code": "US"
        #                 }
        #             }
        #         }
        #     ]
        # }
        # '''


        # Extract relevant details
        # payment_status = response_data.get('status', '')
        # create_time = response_data.get('create_time', '')
        # given_name = response_data.get('payer', {}).get('name', {}).get('given_name', '')
        # surname = response_data.get('payer', {}).get('name', {}).get('surname', '')
        # email_address = response_data.get('payer', {}).get('email_address', '')
        # payer_id = response_data.get('payer', {}).get('payer_id', '')
        # reference_id = response_data.get('purchase_units', [{}])[0].get('reference_id', '')
        # value = response_data.get('purchase_units', [{}])[0].get('amount', {}).get('value', '')
        # currency_code = response_data.get('purchase_units', [{}])[0].get('amount', {}).get('currency_code', '')

        payment_status = request.POST.get('payment_status')
        create_time = request.POST.get('create_time')
        given_name = request.POST.get('given_name')
        surname = request.POST.get('surname')
        email_address = request.POST.get('email_address')
        payer_id = request.POST.get('payer_id')
        reference_id = request.POST.get('reference_id')
        value = request.POST.get('value')
        currency_code = request.POST.get('currency_code')

        # test = request.POST.get['given_name']

        # JSON response to check
        JsonResponse = ({
            'status': payment_status,
            'create_time': create_time,
            'given_name': given_name,
            'surname': surname,
            'email_address': email_address,
            'payer_id': payer_id,
            'reference_id': reference_id,
            'value': value,
            'currency_code': currency_code
        })

        # Create a Payment instance and save it to the database
        payment = Payment.objects.create(
            user=request.user,
            payer_id=payer_id,
            given_name=given_name,
            surname=surname,
            email_address=email_address,
            status=payment_status,
            reference_id=reference_id,
            value=value,
            currency_code=currency_code,
            create_time=create_time
        )

        payment.save() # for saving the Respose
        output = ("Payment processed and stored successfully.")
        return render(request, "templates/payment.html",{'output':output,'JsonResponse':JsonResponse})
    else:
        return render(request, "templates/paymentPaypal.html")


@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user)  # get the login user payment history
    return render(request, "templates/payment-history.html", {'payments': payments})
    # return render(request, "templates/payment-history.html",{'payment':payment})
