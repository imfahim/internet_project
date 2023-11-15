from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render


# Create your views here.
def index(request):
    fxTableData = [
        {'id': 1, 'Name': 'Bitcoin', 'Price': 50000,'oneHrPer': 50000,'twoHrPer': 50000,'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5,'Circulating_Supply': 5},
        {'id': 2, 'Name': 'Bitcoin', 'Price': 50000,'oneHrPer': 50000,'twoHrPer': 50000,'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5,'Circulating_Supply': 5},
        {'id': 3, 'Name': 'Bitcoin',  'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 4, 'Name': 'Bitcoin',  'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 4, 'Name': 'Bitcoin',  'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 5, 'Name': 'Bitcoin',  'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 6, 'Name': 'Bitcoin',  'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},
        {'id': 7, 'Name': 'Bitcoin', 'Price': 50000, 'oneHrPer': 50000, 'twoHrPer': 50000,
         'sevenDayPer': 50000, 'Market_Cap': 1000000000000, 'Volume_24h': 5, 'Circulating_Supply': 5},

    ]
    for rowData in fxTableData:
        # Add a 'change_color' attribute to each entry based on the value of 'change_24h'
        rowData['changeStatus'] = 'positiveChange' if rowData['oneHrPer'] > 0 else 'negativeChange'
        rowData['changeStatus'] = 'positiveChange' if rowData['twoHrPer'] > 0 else 'negativeChange'
        rowData['changeStatus'] = 'positiveChange' if rowData['sevenDayPer'] > 0 else 'negativeChange'

    return render(request, 'internetProject/index.html',{'fxTableData':fxTableData})