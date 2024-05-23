from django.http  import JsonResponse
from .models      import StockRecord, PopulationData
from .Script      import frcast as frcast
from .Script      import regr   as regr

from django.views.decorators.csrf import csrf_exempt

import csv
import io
import json
import math

cmd = {}

def viewStocks(requestParameter):
  stock_records = list(StockRecord.objects.all().values())

  lastStock = stock_records[-1]
  lastYear  = lastStock.get('year')
  lastMonth = lastStock.get('month')

  exogeneous = []
  nextYear   = lastYear 
  for i in range(1, 25):
    nextMonth = (lastMonth + i) % 12

    if nextMonth == 0 :
      nextMonth = 12
    elif nextMonth == 1 :
      nextYear += 1

    data = {
      'month' : nextMonth,
      'year'  : nextYear
    }

    exogeneous.append(data)

  stocks = frcast.predict('stock.model', json.dumps(exogeneous, indent=4))

  predictions = []
  nextMonth   = lastMonth
  nextYear    = lastYear 
  for stock in stocks:
    nextMonth += 1

    if nextMonth == 13 :
      nextMonth = 1
      nextYear += 1

    data = {
      'month'     : nextMonth,
      'year'      : nextYear,
      'avgStock'  : stock
    }

    predictions.append(data)
  
  data = {
    'historical'  : stock_records,
    'prediction'  : predictions
  }

  return send(True, 'ok', data)
cmd['fetch-stock'] = viewStocks

def viewConsumption(requestParameter):
  population_data = list(PopulationData.objects.all().values())

  lastYear = population_data[-1].get('year')

  predictNext1 = lastYear + 1
  predictNext2 = lastYear + 2

  predictions = []
  predictions.append(regr.predict('population.model', 'consumption.model', predictNext1))
  predictions.append(regr.predict('population.model', 'consumption.model', predictNext2))

  data = {
    'historical'  : population_data,
    'prediction'  : predictions
  }

  return send(True, 'ok', data)
cmd['fetch-consumption'] = viewConsumption

def insertStock(requestParameter) :
  year     = requestParameter('param0')
  month    = requestParameter('param1')
  avgStock = math.sqrt(requestParameter('param2'))

  StockRecord.objects.create(year, month, avgStock)

  data = json.dumps(list(StockRecord.objects.all().values()), indent=4)
  frcast.train(data, 'stock.model')  
cmd['insert-stock'] = insertStock

def bulkStockInsert(requestParameter) :
  file_stream = io.TextIOWrapper(requestParameter['paramFile'].file, encoding='utf-8')
  csvreader   = csv.DictReader(file_stream)
  listreader  = list(csvreader)
      
  for row in listreader:
    month    = row['month']
    year     = row['year']
    avgStock = row['stock']

    StockRecord.objects.create(year, month, avgStock)
    
  data = json.dumps(list(StockRecord.objects.all().values()), indent=4)
  frcast.train(data, 'stock.model')

  return send(True, 'ok')
cmd['insert-stock-bulk'] = bulkStockInsert

def insertConsumption(requestParameter):
  year            = requestParameter('param0')
  population      = requestParameter('param1')
  consumptionRate = math.sqrt(requestParameter('param2'))

  PopulationData.objects.create(year, population, consumptionRate)

  data = json.dumps(list(PopulationData.objects.all().values()), indent=4)
  regr.train(data, 'population.model', 'consumption.model')

  return send(True, 'ok', None)
cmd['insert-consumption'] = insertConsumption

def bulkConsumptionInsert(requestParameter) :
  file_stream = io.TextIOWrapper(requestParameter['paramFile'].file, encoding='utf-8')
  csvreader   = csv.DictReader(file_stream)
  listreader = list(csvreader)
        
  for row in listreader:
    year        = row['year']
    population  = row['population']
    consumptionRate = row['consumption']

    PopulationData.objects.create(year, population, consumptionRate)

  data = json.dumps(list(PopulationData.objects.all().values()), indent=4)
  regr.train(data, 'population.model', 'consumption.model')

  return send(200, 'ok', None)
cmd['insert-consumption-bulk'] = bulkConsumptionInsert

# -----=== Auto controller ===-----

def send(status, message , data={}):
  data = {
    'status'    : status,
    'message' : message,
    'data'    : data
  }
  
  return JsonResponse(data)

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
      
      requestParameter[param_key] = param_value
 
      param_index += 1
  
  if request.method == 'POST':
    requestParameter['paramFile'] = request.FILES.get('file')

  return executor(command, requestParameter)

def executor(function_name, *args, **kwargs):
  func = cmd.get(function_name)

  if func:
      return func(*args, **kwargs)
  else:
      return send(False, 'Bad Request', None)