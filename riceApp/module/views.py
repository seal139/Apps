from django.http     import HttpResponse
from django.template import loader
from django.http     import JsonResponse

import json

# Views
def index(request):
  template = loader.get_template('pages/dashboard.html')
  return HttpResponse(template.render())