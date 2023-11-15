from django.shortcuts import render

# Create your views here.hghghg

def index(request):
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
    response.write("Name:", data["name"])
    response.write("Symbol:", data["symbol"])
    response.write("Price:", f"${data['quotes']['USD']['price']}")
    response.write("1h %:", f"{data['quotes']['USD']['percent_change_1h']}%")
    response.write("24h %:", f"{data['quotes']['USD']['percent_change_24h']}%")
    response.write("7d %:", f"{data['quotes']['USD']['percent_change_7d']}%")
    response.write("Market Cap:", f"${data['quotes']['USD']['market_cap']}")
    response.write("Volume (24h):", f"${data['quotes']['USD']['volume_24h']}")
    response.write("Circulating Supply:", f"{data['circulating_supply']} {data['symbol']}")
    response.write("Last 7 Days:", f"{data['quotes']['USD']['percent_change_7d']}%")
    return response;

