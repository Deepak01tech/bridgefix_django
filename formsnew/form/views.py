# from urllib import request
from django.shortcuts import render

# Create your views here.

from .forms import InputForm
def home_view(request):
    # form = InputForm()
    context= {}
    context['form'] = InputForm()


    return render(request, 'home.html', context)
