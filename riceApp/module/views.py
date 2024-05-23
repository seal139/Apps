from django.http     import HttpResponse
from django.template import loader
from django.http     import JsonResponse
from .models         import StockRecord, PopulationData

import json

# Views
def index(request):
  template = loader.get_template('pages/dashboard.html')
  return HttpResponse(template.render())

# API Gateway
def api(request):
  requestParameter = {}
  fileParam        = None
  command          = None

  command = request.GET.get('cmd') or request.POST.get('cmd')

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


def send(code, outMessage):
  data = {
    'code'      : code,
    'outMessage': outMessage
  }
  
  return JsonResponse(data)


def insertStock(year, month, avg_stock, stock_type):
  StockRecord.objects.create(year=year, month=month, avgStock=avg_stock, type=stock_type)

def insertPopulation(year, population, consumption_rate):
  PopulationData.objects.create(year=year, population=population, consumptionRate=consumption_rate)

def view_stock_records():
  stock_records = list(StockRecord.objects.all().values())
  return json.dumps(stock_records, indent=4)

def view_population_data():
  population_data = list(PopulationData.objects.all().values())
  return json.dumps(population_data, indent=4)