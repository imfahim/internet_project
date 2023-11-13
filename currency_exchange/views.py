from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import requests


# Create your views here.
def currency(request, from_currency, to_currency):
    rate = get_exchange_rate(from_currency, to_currency)
    return JsonResponse({'rate': rate})


def get_exchange_rate(from_currency, to_currency):
    # 假设您已将API密钥存储在Django的settings文件中
    api_key = settings.EXCHANGE_RATE_API_KEY
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"

    # try:

    response = requests.get(url)
    response.raise_for_status()  # 将触发HTTPError，如果请求返回4xx或5xx响应
    data = response.json()

    # 解析JSON数据以获取汇率
    rates = data.get('rates', {})
    rate = rates.get(to_currency)
    if rate:
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
