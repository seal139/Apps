from django.http     import JsonResponse
from .models         import StockRecord, PopulationData
from .Script         import frcast as frcast
from .Script         import regr   as regr

import csv
import io
import json

# API Gateway
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
    fileParam = request.FILES.get('fileInp')

def route(command, requestParameter, fileParam):
    
  if command == 'fetch-stock' :
    return send(200, 'ok', viewStocks())
  
  if command == 'fetch-consumption' :
    return send(200, 'ok', viewConsumption())


  if command == 'insert-consumption' :
    insertPopulation(requestParameter('param0'), requestParameter('param1'), requestParameter('param2'))

    data = json.dumps(list(PopulationData.objects.all().values()), indent=4)
    regr.train(data, 'population.model', 'consumption.model')

    return send(200, 'Ok', None)
  
  if command == 'insert-consumption-bulk' :
    file_stream = io.TextIOWrapper(fileParam.file, encoding='utf-8')
    csvreader   = csv.DictReader(file_stream)
        
    for row in csvreader:
      year        = row['year']
      population  = row['population']
      consumption = row['consumption']

      insertPopulation(year, population, consumption)

    data = json.dumps(list(PopulationData.objects.all().values()), indent=4)
    regr.train(data, 'population.model', 'consumption.model')

    return send(200, 'Ok', None)

  if command == 'insert-stock' :
    insertStock(requestParameter('param0'), requestParameter('param1'), requestParameter('param2'), True)

    data = json.dumps(list(StockRecord.objects.all().values()), indent=4)
    frcast.train(data, 'stock.model')
  
    return send(200, 'Ok')
  
  if command == 'insert-stock-bulk' :


  if command == 'delete-stock' :
    return send(200, 'Ok')

  if command == 'delete-consumption' :
    return send(200, 'Ok')

  if command == 'update-stock' :
    return send(200, 'Ok')

  if command == 'update-consumption' :
    return send(200, 'Ok')
  
  return send(400, 'Bad Request')

def send(code, message , data):
  data = {
    'code'    : code,
    'message' : message,
    'data'    : data
  }
  
  return JsonResponse(data)

def insertStock(year, month, avg_stock, stock_type):
  StockRecord.objects.create(year=year, month=month, avgStock=avg_stock, type=stock_type)

def insertPopulation(year, population, consumption_rate):
  PopulationData.objects.create(year=year, population=population, consumptionRate=consumption_rate)

def viewStocks():
  stock_records = list(StockRecord.objects.all().values())

  lastStock = stock_records[-1]
  lastYear  = lastStock.get('year')
  lastMonth = lastStock.get('month')

  exogeneous = []
  for i in range(1, 25):
    nextMonth = lastMonth + i
    nextYear  = lastYear 

    if nextMonth == 13 :
      nextMonth = 1
      nextYear += 1

    data = {
      'month' : nextMonth,
      'year'  : nextYear
    }

    exogeneous.append(data)

  predictions = frcast.predict('stock.model', json.dumps(exogeneous, indent=4))
  
  data = {
    'historical'  : json.dumps(stock_records, indent=4),
    'prediction'  : predictions
  }

  return data #son.dumps(stock_records, indent=4)

def viewConsumption():
  population_data = list(PopulationData.objects.all().values())

  lastYear = population_data[-1].get('year')

  predictNext1 = lastYear + 1
  predictNext2 = lastYear + 2

  predictions = []
  predictions.append(regr.predict('population.model', 'consumption.model', predictNext1))
  predictions.append(regr.predict('population.model', 'consumption.model', predictNext2))

  data = {
    'historical'  : json.dumps(population_data, indent=4),
    'prediction'  : json.dumps(predictions, indent=4)
  }

  return data