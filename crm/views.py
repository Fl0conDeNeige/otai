from django.http import HttpResponse
from django.views.generic import View

from .models import User

def index(request):
    return HttpResponse("Hello, world.")
