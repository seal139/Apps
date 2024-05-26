from .ml  import stockPredictor        as StockPredictor
from .ml  import consumptionPredictor  as ConsumptionPredictor
from .dao import consumptionController as ConsumptionController
from .dao import stockController       as StockController

from django.http  import JsonResponse
from .models      import Stock, Consumption

from django.views.decorators.csrf import csrf_exempt

import csv
import io
import json
import math

slugPost = {}
slugGet  = {}

# ==================-----------
# Stock Data
# ==================-----------

def bulkStockInsert(requestParameter) :
    listreader = __readFile(requestParameter)
    msg        = StockController.bulkInsert(listreader)
    if msg != None :
        return __send(msg, None)
    #end if
        
    __trainStock()

    return __send(None, None)
slugPost['insert-stock-bulk'] = bulkStockInsert
#end def

def insertStock(requestParameter) :
    msg = StockController.insert(requestParameter)
    
    if msg != None :
        return __send(msg, None)
    #end if

    __trainStock()

    return __send(None, None)
slugPost['insert-stock'] = insertStock
#end def

def updateStock(requestParameter):
    msg = StockController.update(requestParameter)
    
    if msg != None :
        return __send(msg, None)
    #end if
    
    __trainStock()

    return __send(None, None)
slugPost['update-stock'] = updateStock
#end def

def deleteStock(requestParameter) :
    msg = StockController.delete(requestParameter)
    
    if msg != None :
        return __send(msg, None)
    #end if

    __trainStock()

    return __send(None, None)
slugPost['delete-stock'] = deleteStock
#end def

def viewStocks(requestParameter):
    stock_records = StockController.select()

    if stock_records == None:
        return __send(None, None)

    lastStock = stock_records[-1]
    lastYear  = lastStock['year']
    lastMonth = lastStock['month']

    exogeneous = []
    nextYear   = lastYear 
    for i in range(1, 25):
        nextMonth = (lastMonth + i) % 12

        if nextMonth == 0 :
            nextMonth = 12
        elif nextMonth == 1 :
            nextYear += 1
        #end if

        data = {
            'month' : nextMonth,
            'year'  : nextYear
        }

        exogeneous.append(data)
    #end for

    stocks = StockPredictor.predict('stock.model', json.dumps(exogeneous, indent=4))

    predictions = []
    nextMonth   = lastMonth
    nextYear    = lastYear 
    id          = 0
    for stock in stocks:
        nextMonth += 1

        if nextMonth == 13 :
            nextMonth = 1
            nextYear += 1
        #end if

        id += 1
        data = {
            'id'        : id,
            'year'      : nextYear,
            'month'     : nextMonth,
            'avgStock'  : stock ** 2
        }

        predictions.append(data)
    #end for

    data = {
        'historical'  : stock_records,
        'prediction'  : predictions
    }

    return __send(None, data)
slugGet['fetch-stock']  = viewStocks
slugPost['fetch-stock'] = viewStocks
#end def


# ==================-----------
# Consumption Data
# ==================-----------

def bulkConsumptionInsert(requestParameter) :
    listreader = __readFile(requestParameter)
    msg        = ConsumptionController.bulkInsert(listreader)
    if msg != None :
        return __send(msg, None)
    #end if

    __trainConsumption()

    return __send(msg, None)
slugPost['insert-consumption-bulk'] = bulkConsumptionInsert
#end def

def insertConsumption(requestParameter):
    msg = ConsumptionController.insert(requestParameter)

    if msg != None :
        return __send(msg, None)
    #end if

    __trainConsumption()

    return __send(None, None) 
slugPost['insert-consumption'] = insertConsumption
#end if

def updateConsumption(requestParameter) :
    msg = ConsumptionController.update(requestParameter)

    if msg != None :
        return __send(msg, None)
    #end if

    __trainConsumption()

    return __send(None, None) 
slugPost['update-consumption'] = updateConsumption
#end def

def deleteConsumption(requestParameter) :
    msg = ConsumptionController.delete(requestParameter)

    if msg != None :
        return __send(msg, None)
    #end if

    __trainConsumption()

    return __send(None, None)
slugPost['delete-consumption'] = deleteConsumption
#end def

def viewConsumption(requestParameter):
    population_data = ConsumptionController.select()

    if population_data == None:
        return __send(None, None)

    lastYear = population_data[-1]['year']

    predictNext1 = lastYear + 1
    prediction1 = ConsumptionPredictor.predict('population.model', 'consumption.model', predictNext1)

    print (prediction1)
    data1 = {
        'id'          : 1,
        'year'        : predictNext1,
        'population'  : prediction1[0] ** 2,
        'consumption' : prediction1[1] ** 2
    }

    predictNext2 = lastYear + 2
    prediction2 = ConsumptionPredictor.predict('population.model', 'consumption.model', predictNext2)
    data2 = {
        'id'          : 2,
        'year'        : predictNext2,
        'population'  : prediction2[0] ** 2,
        'consumption' : prediction2[1] ** 2
    }

    data = {
        'historical'  : population_data,
        'prediction'  : [data1, data2]
    }

    return __send(None, data)
slugGet['fetch-consumption']  = viewConsumption
slugPost['fetch-consumption'] = viewConsumption
#end def

# -----=== Auto controller ===-----

def __readFile(requestParameter) -> list :
    file_stream = io.TextIOWrapper(requestParameter['paramFile'].file, encoding='utf-8')
    csvreader   = csv.DictReader(file_stream)
    listreader = list(csvreader)

    return listreader
#end def

def __trainStock() :
    data = json.dumps(list(Stock.objects.all().values()), indent=4)
    StockPredictor.train(data, 'stock.model')
#end def

def __trainConsumption() :
    data = json.dumps(list(Consumption.objects.all().values()), indent=4)
    ConsumptionPredictor.train(data, 'population.model', 'consumption.model')
#end def

def __send(message , data={}):
    if message == None :
        response = {
            'status'  : True,
            'message' : 'Success',
            'data'    : data
        }
        return JsonResponse(response)
    #end if

    response = {
        'status'  : False,
        'message' : message,
        'data'    : None
    }
    return JsonResponse(response)
#end def

def __executor(function_name, post, *args, **kwargs):
    func = None
    if post :
        func = slugPost.get(function_name)
    else :
        func = slugGet.get(function_name)
    #end if

    if func:
        return func(*args, **kwargs)
    else:
        return __send(False, 'Bad Request', None)
    #end if
#end def
    
# API Gateway
@csrf_exempt
def api(request, command):
    requestParameter = {}
    fileParam        = None

    param_index = 0
    while True:
        param_key   = f'param{param_index}'
        param_value = request.GET.get(param_key) or request.POST.get(param_key)
        if param_value is None:
            break
        #end if
        
        requestParameter[param_key] = param_value

        param_index += 1
    #end while

    if request.method == 'POST':
        if 'file' in request.FILES :
            requestParameter['paramFile'] = request.FILES['file']
        #end if

        return __executor(command, True, requestParameter)
    else :
        return __executor(command, False, requestParameter)
    #end if
#end def