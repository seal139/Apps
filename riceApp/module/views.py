from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

# Views
def index(request):
  template = loader.get_template('pages/dashboard.html')
  return HttpResponse(template.render())

# API Gateway
def members(request):
  requestParameter = {}
  fileParam        = None
  command          = None

  command = request.GET.get('cmd') or request.POST.get('cmd')

  param_index = 0
  while True:
      param_key = f'param{param_index}'
      param_value = request.GET.get(param_key) or request.POST.get(param_key)
      if param_value is None:
          break
      
      requestParameter[param_key] = param_value
      param_index += 1
  
  if request.method == 'POST':
    fileParam = request.FILES.get('fileInp')

def setupDb():
  
  
  data = {
    'requestParameter': requestParameter,
    'fileParam': fileParam.name if fileParam else None,
    'command': command,
  }
  
  return JsonResponse(data)
