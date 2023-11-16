from _decimal import Decimal

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from .models import Currency_rate
import requests
from datetime import datetime
import pytz


# Create your views here.
def currency(request, from_currency, to_currency):
    rate = get_exchange_rate(from_currency, to_currency)
    # get current time
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.now(pytz.utc).astimezone(eastern).isoformat()
    now_rates = Currency_rate.objects.filter(from_currency=from_currency, to_currency=to_currency).order_by('-time')[:10]


    # return JsonResponse({'rate': rate})
    return render(request, 'currency.html', {'rate': rate, 'from_currency': from_currency, 'to_currency': to_currency
        , 'current_time': current_time , 'now_rates': now_rates})


def get_exchange_rate(from_currency, to_currency):
    # 假设您已将API密钥存储在Django的settings文件中
    api_key = settings.EXCHANGE_RATE_API_KEY
    url = f"https://min-api.cryptocompare.com/data/price?fsym={from_currency}&tsyms={to_currency}&api_key={api_key}"

    # try:
    response = requests.get(url)
    response.raise_for_status()  # 将触发HTTPError，如果请求返回4xx或5xx响应
    data = response.json()

    # # 解析JSON数据以获取汇率
    # rates = data.get('rates', {})
    # rate = rates.get(from_currency)
    rate = data.get(to_currency)
    if rate:
        # get current time
        rate = Decimal(rate).quantize(Decimal('.000001'))
        est = pytz.timezone('US/Eastern')
        current_time_est = datetime.now().astimezone(est)
        # put the rate into the database for future use
        Currency_rate.objects.create(from_currency=from_currency, to_currency=to_currency, rate=rate,
                                     time=current_time_est)
        return rate
    else:
        raise ValueError("Currency not found.")
    # except requests.exceptions.HTTPError as errh:
    #     print("Http Error:", errh)
    # except requests.exceptions.ConnectionError as errc:
    #     print("Error Connecting:", errc)
    # except requests.exceptions.Timeout as errt:
    #     print("Timeout Error:", errt)
    # except requests.exceptions.RequestException as err:
    #     print("Oops: Something Else", err)

def index(request):
    return render(request,"index.html")



def payment(request):
    return render(request,"payment.html")
